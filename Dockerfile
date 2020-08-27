FROM ubuntu:16.04

MAINTAINER UMass Robotics "roboticsumass@gmail.com"

RUN 	apt-get update -y && \
	apt-get install -y python-pip python-dev && \
	pip install --upgrade pip
	

COPY . /src

WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 8081

CMD cd /src && python server.py