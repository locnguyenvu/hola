FROM python:3.8-alpine3.12

WORKDIR /src

COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3
RUN pip3 install -r requirements.txt

ENV FLASK_APP="api"
ENV FLASK_DEBUG=0

#CMD ["flask", "run"]
