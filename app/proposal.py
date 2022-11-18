from jinja2 import Template
import pdfkit
import logging
import datetime
import os
from flask import Flask, request
import schedule

ROOT_URL = os.environ.get("ROOT_URL", "http://localhost")

app = Flask(__name__, static_url_path='/static')
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route("/check",methods=['GET'])
def health_check():
    return "CHECK WORKING"

@app.route("/",methods=['POST'])
def make_proposal():
    body = request.json
    with open('./template.html') as f:
        jinja_t = Template(f.read())
    rendered = jinja_t.render(data=body)
    ts = datetime.datetime.now().timestamp()
    if (not os.path.exists('./static')):
        os.makedirs('./static')
    pdfkit.from_string(rendered, f"./static/proposal_{ts}.pdf")

    response = {
            'statusCode': 200,
            'body': {"proposal" : f"{ROOT_URL}/static/proposal_{ts}.pdf"}
        }
    return response

def clean_static():
    count = 0
    for file in os.listdir('./static'):
        count += 1
        os.remove(file)
    print("Cleaned static files: ", count)


if __name__ == '__main__':
    schedule.every().sunday.at("01:00").do(clean_static)
    app.run(host='0.0.0.0', port=80)