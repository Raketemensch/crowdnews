FROM ubuntu:20.04

MAINTAINER fnord "fnord@libertylost.org

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip mongodb-server cron vim

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY app_crontab /etc/cron.d/app_crontab

RUN touch /var/log/cron.log

RUN chmod 0644 /etc/cron.d/app_crontab &&\
    crontab /etc/cron.d/app_crontab

COPY . /app

ENTRYPOINT [ "./start.sh" ]
