FROM mcr.microsoft.com/devcontainers/python:0-3.11

ENV PYTHONUNBUFFERED 1

ENV TZ="America/New_York"
RUN date

RUN pip install --upgrade pip

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends default-mysql-client ack bash-completion unixodbc unixodbc-dev \
     build-essential libssl-dev libffi-dev freetds-dev freetds-bin unixodbc-dev tdsodbc

RUN sudo bash -c "echo -e '[FreeTDS]\nDescription=FreeTDS Driver\nDriver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\
\nSetup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so' >> /etc/odbcinst.ini"

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp
