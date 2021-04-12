import fitz
import sys
import os 
import requests
import boto3
import json
from random import randint
from PIL import Image, ImageOps
import json
import base64
s3 = boto3.client('s3')


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
    with fitz.open(document) as doc:
        first_page = doc[0]
        third_page = doc[page]
        third_page_image = third_page.getPixmap(alpha = False).writePNG("/tmp/discount_page.png") 
        cropped = Image.open("/tmp/discount_page.png").crop((40,50,300,100)).save("/tmp/cropped.png") 
        ImageOps.expand(Image.open('/tmp/cropped.png'),border=15,fill='red').save('/tmp/cropped.png')
        first_page.insertImage(fitz.Rect(40,50,300,100),pixmap=fitz.Pixmap("/tmp/cropped.png"), overlay=True)
        doc.save("/tmp/SIGNED_CONTRACT_w_discount.pdf")

def create_our_file(contract_name, proposal_name):
    add_discount(2,contract_name)

    splitted_contract = file_split("/tmp/SIGNED_CONTRACT_w_discount.pdf", "/tmp/CONTRACT")
    splitted_proposal = file_split(proposal_name, "/tmp/PROPOSAL")
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
    final_file.save("/tmp/final.pdf",garbage=4, deflate=True)
    

def handler(event, context):
    print(event)
    body = json.loads(event['body'])
    print(body)
    r = requests.get(body['contract'])
    open('/tmp/SIGNED_CONTRACT.pdf', 'wb').write(r.content)
    r = requests.get(body['proposal'])
    open('/tmp/proposal.pdf', 'wb').write(r.content)
    create_our_file("/tmp/SIGNED_CONTRACT.pdf","/tmp/proposal.pdf")
    os.system("pdfjam --nup 2x1 --landscape /tmp/final.pdf --outfile /tmp/output.pdf")
    f = open("/tmp/output.pdf", "rb")
    read_bytes = f.read()
    response = {
            'statusCode': 200,
            'body': base64.b64encode(read_bytes).decode('utf-8'),
            'isBase64Encoded': True
        }
    return json.dumps(response)

