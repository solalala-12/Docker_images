# 베이스 이미지로 ubuntu18:04 사용
FROM ubuntu:18.04

# 메인테이너 정보 (옵션)
MAINTAINER sora charmingsora12@gmail.com

# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN apt-get install -y git

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

# Python package management and basic dependencies
RUN apt-get install -y curl python3.6 python3.6-dev python3.6-distutils

# Install dependencies
RUN apt install python3-pip
RUN pip3 install tensorflow==1.3
RUN pip3 install FFmpeg

ADD requirements.txt /dc/python-docker/
RUN pip3 install -r /dc/python-docker/requirements.txt

CMD tail -f /dev/null
WORKDIR /dc/python-docker
