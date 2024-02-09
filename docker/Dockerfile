FROM python:3.12-alpine

RUN apk add --update nodejs npm \
 && npm install -g cdk

VOLUME /source

WORKDIR /source

CMD sh