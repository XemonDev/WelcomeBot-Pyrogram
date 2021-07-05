FROM ubuntu:latest
FROM python:3.9.5-buster
RUN apt update && apt upgrade -y
RUN pip3 install -U pip
COPY . /app
WORKDIR /app
RUN pip3 install -U -r requirements.txt
CMD python3 -m Welcome-Bot