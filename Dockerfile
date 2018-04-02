# alpine-python-ecmwfapi
FROM python:alpine

MAINTAINER epmorris "edward.morris@eo4.eu"

WORKDIR /usr/src/app

RUN pip install pytest-shutil
RUN pip install --upgrade google-api-python-client

COPY . .
