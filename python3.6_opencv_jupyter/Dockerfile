FROM python:3.6

WORKDIR /home/recog_cardnum


ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip 

RUN pip3 install jupyter
ADD config/jupyter/jupyter_notebook_config.py /root/.jupyter/
RUN mkdir /root/.jupyter/custom
RUN echo '.CodeMirror pre {font-family: Inconsolata-g; font-size: 12pt; line-height: 140%;}\n.container { width:100% !important; }\ndiv.output pre{\n    font-family: Inconsolata-g;\n    font-size: 12pt;\n}' >> /root/.jupyter/custom/custom.css


RUN pip3 install imutils
RUN pip3 install numpy
RUN pip3 install argparse
RUN pip3 install imutils
RUN pip3 install opencv-python


