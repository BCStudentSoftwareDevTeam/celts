FROM mcr.microsoft.com/devcontainers/python:0-3.11

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends 

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends mysql-client
     
# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
RUN pip3 --disable-pip-version-check --no-cache-dir 