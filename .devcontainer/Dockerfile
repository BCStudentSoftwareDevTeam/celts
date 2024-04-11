FROM mcr.microsoft.com/devcontainers/python:0-3.11

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends default-mysql-client ack