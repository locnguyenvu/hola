FROM python:alpine

WORKDIR /src

COPY setup.py .
RUN apk add --no-cache --virtual .build-deps g++ libffi-dev openssl-dev 
RUN python -m pip install -e . 

COPY config.py .
COPY wsgi.py .
COPY app ./app

CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol", "http", "-w","wsgi:hola_api"]
