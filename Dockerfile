FROM ubuntu:16.04
MAINTAINER toolbox@cloudpassage.com

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python-pip

RUN pip install codeclimate-test-reporter
