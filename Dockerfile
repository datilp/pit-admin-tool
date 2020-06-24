FROM python:3.7-alpine
MAINTAINER Igor Sola

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev libffi-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk add --update nodejs npm
RUN apk del .tmp-build-deps
RUN npm install create-react-app --global

RUN mkdir /project
WORKDIR /project
COPY ./project /project

RUN adduser -D adminpit

USER adminpit

#ENV PATH="/admin_app/node_modules/:${PATH}"
