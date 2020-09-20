FROM pdfer

WORKDIR /app

RUN pip3 install requests boto3 pillow uwsgi
COPY . .

EXPOSE 3000

CMD ["uwsgi", "--http", ":3000", "--wsgi-file", "app.py", "--callable", "app"]