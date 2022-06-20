FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  wget \
  python3-pip

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb

RUN pip3 install --target "/app" awslambdaric pdfkit flask boto3

COPY app/ app/

WORKDIR /app

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "dockerProposal.make_proposal" ]