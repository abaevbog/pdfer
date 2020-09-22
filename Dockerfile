FROM 612185335394.dkr.ecr.us-east-1.amazonaws.com/pdfer_template

WORKDIR /app
RUN apt install -y python3-pip
RUN pip3 install requests boto3 pillow uwsgi PyMuPDF flask
COPY . .

EXPOSE 3000

CMD ["uwsgi", "--http", ":3000", "--wsgi-file", "app.py", "--callable", "app"]