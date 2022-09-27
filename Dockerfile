FROM ubuntu:20.04

RUN apt update && apt install -y wget python3-pip

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb

RUN pip3 install pdfkit flask requests schedule

COPY app/ app/

WORKDIR /app

EXPOSE 80 443

CMD ["python3", "./proposal.py"]
