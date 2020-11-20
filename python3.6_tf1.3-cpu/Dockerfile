# 베이스 이미지로 ubuntu18:04 사용
FROM ubuntu:18.04

WORKDIR /home/multi-speaker-tacotron


# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y 
# RUN apt-get clean

# Install python3 / python3 pip
RUN apt-get install -y build-essential python3 python3-pip 
RUN apt-get upgrade python3 -y
RUN apt-get install git -y

# Install packages
RUN pip3 install tensorflow==1.3
RUN pip3 install FFmpeg

# container
RUN mkdir sources
# local / container
ADD sources/requirements.txt /home/multi-speaker-tacotron/sources
RUN pip3 install -r /home/multi-speaker-tacotron/sources/requirements.txt

