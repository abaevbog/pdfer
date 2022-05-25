
# Define function directory
ARG FUNCTION_DIR="/app"

FROM python:buster as build-image

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  wkhtmltopdf \
  python3-pip

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY app/* ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric \
        requests \
        boto3 \
        pdfkit \ 
        jinja2

# Multi-stage build: grab a fresh copy of the base image
#FROM python:buster
#RUN apt-get update && \
#  apt-get install -y \
#  wkhtmltopdf
  
# Include global arg in this stage of the build
#ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
#COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "proposal.handler" ]