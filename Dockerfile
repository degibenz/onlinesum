FROM python:3.5

MAINTAINER alexey shkil

RUN apt-get -y update

RUN apt-get install -y python-dev python-pip python3-pip

ADD requirments.txt /home/requirments.txt

RUN pip3 install -r /home/requirments.txt