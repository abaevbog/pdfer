from jinja2 import Template
import pdfkit
import random
import json 
import boto3
import datetime

BUCKET = "basementremodeling-archive-12345"
s3 = boto3.client('s3')

def handler(event, context):
    body = json.loads(event['body'])
    categories = body['categories']
    with open('proposalTemplate.html') as f:
        template = f.read()
        jinja_t = Template(template)
        rendered = jinja_t.render(categories=categories)
        pdfkit.from_string(rendered, '/tmp/proposal.pdf')
    ts = datetime.datetime.now().timestamp()
    with open("/tmp/proposal.pdf", "rb") as f:
        s3.upload_fileobj(f, BUCKET, f"temp/proposal_{ts}.pdf",ExtraArgs={'ACL':'public-read'} )

    response = {
            'statusCode': 200,
            'body': {"proposal" : f"https://{BUCKET}/temp/proposal_{ts}.pdf"}
        }
    return json.dumps(response)
