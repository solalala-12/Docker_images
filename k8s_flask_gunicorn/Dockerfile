FROM ubuntu:18.04


WORKDIR /root/model_rest_api

RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y build-essential python3.7 python3-pip 
RUN pip3 install --upgrade pip

ADD requirements.txt /root/model_rest_api/requirements.txt
RUN apt-get install rabbitmq-server -y
RUN pip3 install -r /root/model_rest_api/requirements.txt

ENV LANG C.UTF-8 
EXPOSE 5000
EXPOSE 5672

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
