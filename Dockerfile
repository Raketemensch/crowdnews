FROM ubuntu:20.04

MAINTAINER fnord "fnord@libertylost.org

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip mongodb-server

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]