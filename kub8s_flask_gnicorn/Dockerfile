FROM ubuntu:18.04
WORKDIR /root/flask_api_demo
COPY . /root/flask_api_demo

RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y build-essential python3.7 python3-pip 
RUN apt-get install sudo
RUN apt-get install vim -y

RUN apt-get install rabbitmq-server -y
RUN pip3 install -r /root/flask_api_demo/requirements.txt


ENV LANG C.UTF-8 
EXPOSE 5000
EXPOSE 5672

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

ADD start_celery.sh .
RUN sh start_celery.sh
