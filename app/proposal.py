from jinja2 import Template
import pdfkit
import logging
import requests 
import boto3
import datetime
from flask import Flask, request
BUCKET = "basementremodeling-archive-12345"
s3 = boto3.client('s3')
TEMPLATE_URL = "https://basementremodeling-com-estimation-tool.s3.amazonaws.com/static/template.html"

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route("/check",methods=['GET'])
def health_check():
    return "CHECK"

@app.route("/",methods=['POST'])
def make_proposal():
    body = request.json
    r = requests.get(TEMPLATE_URL)
    jinja_t = Template(r.text)
    rendered = jinja_t.render(data=body)
    pdfkit.from_string(rendered, '/tmp/proposal.pdf')

    ts = datetime.datetime.now().timestamp()
    with open("/tmp/proposal.pdf", "rb") as f:
       s3.upload_fileobj(f, BUCKET, f"temp/proposal_{ts}.pdf",ExtraArgs={'ACL':'public-read'} )

    response = {
            'statusCode': 200,
            'body': {"proposal" : f"https://{BUCKET}.s3.amazonaws.com/temp/proposal_{ts}.pdf"}
        }
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)