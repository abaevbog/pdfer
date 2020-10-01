import fitz
import sys
import os 
from flask import Flask
import requests
import boto3
from flask import request
import json
from random import randint
from PIL import Image, ImageOps
s3 = boto3.client('s3')

app = Flask(__name__)


def file_split(file_name, comment):
    doc = fitz.open(file_name)
    arr = []
    index = 0
    while index < len(doc):
        if len(doc[index].getText()) > 7:
            new_page = fitz.open() 
            new_page.insertPDF(doc,from_page = index,to_page = index)
            p = fitz.Point(500, 20)
            new_page[0].insertText(p,  # bottom-left of 1st char
                                comment,  # the text (honors '\n')
                                fontname = "helv",  # the default font
                                fontsize = 20,  # the default font size
                                rotate = 0,  # also available: 90, 180, 270
                                )
            arr.append(new_page)
        index += 1
    return arr



def add_discount(page, document):
    text = 'DISCOUNT: '
    with fitz.open(document) as doc:
        first_page = doc[0]
        third_page = doc[page]
        third_page_image = third_page.getPixmap(alpha = False).writePNG("discount_page.png") 
        cropped = Image.open("discount_page.png").crop((40,50,300,100)).save("cropped.png") 
        ImageOps.expand(Image.open('cropped.png'),border=15,fill='red').save('cropped.png')
        first_page.insertImage(fitz.Rect(40,50,300,100),pixmap=fitz.Pixmap("cropped.png"), overlay=True)
        doc.save("SIGNED_CONTRACT_w_discount.pdf")

def create_our_file(contract_name, proposal_name):
    add_discount(2,"SIGNED_CONTRACT.pdf")

    splitted_contract = file_split("SIGNED_CONTRACT_w_discount.pdf", "CONTRACT")
    splitted_proposal = file_split(proposal_name, "PROPOSAL")
    splitted_scope = splitted_contract[8:-1]

    array_to_merge = [splitted_contract[0],splitted_proposal[-1],splitted_contract[8],splitted_proposal[0]]
    i = 1
    while i < len(splitted_scope) and i < len(splitted_proposal):
        array_to_merge += [splitted_scope[i], splitted_proposal[i]]
        i += 1

    while i < len(splitted_scope):
        new = fitz.open()
        new.insertPage(pno=0)
        array_to_merge += [splitted_scope[i], new]
        i += 1
        
    while i < len(splitted_proposal):
        new = fitz.open()
        new.insertPage(pno=0)
        array_to_merge += [new, splitted_proposal[i]]
        i += 1
    final_file = fitz.open()
    for document in array_to_merge:
        final_file.insertPDF(document)
    final_file.save("final.pdf",garbage=4, deflate=True)
    
@app.route('/',methods=['POST'])
def do_stuff():
    r = requests.get(request.json['contract'])
    open('SIGNED_CONTRACT.pdf', 'wb').write(r.content)
    r = requests.get(request.json['proposal'])
    open('proposal.pdf', 'wb').write(r.content)
    create_our_file("SIGNED_CONTRACT.pdf","proposal.pdf")
    os.system("pdfjam --nup 2x1 --landscape final.pdf --outfile output.pdf")
    with open("output.pdf", "rb") as f:
        rand = randint(0,1000)
        s3.upload_fileobj(f, "basementremodeling-archive-12345", f"outputs/scope_with_proposal_{rand}.pdf", {"ACL":"public-read"})
    os.system("rm *.pdf")
    os.system("rm *.png")
    return json.dumps({"file_url": f"https://basementremodeling-archive-12345.s3.amazonaws.com/outputs/scope_with_proposal_{rand}.pdf"})

@app.route('/health',methods=['GET','POST'])
def health():
    return "Ok"