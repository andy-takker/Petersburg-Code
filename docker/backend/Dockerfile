FROM almalinux:8.6

RUN dnf update -y && dnf install wget yum-utils make gcc openssl-devel bzip2-devel libffi-devel zlib-devel sqlite-devel -y
RUN wget https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz && tar xzf Python-3.10.2.tgz
WORKDIR /Python-3.10.2
RUN ./configure --with-system-ffi --with-computed-gotos --enable-loadable-sqlite-extensions && make && make altinstall

WORKDIR /backend
ADD /docker/backend/requirements.txt /
RUN python3.10 -m pip install -r /requirements.txt --no-cache-dir
ARG DEBUG
ARG VERSION
ARG SERVER_NAME
ARG PROJECT_NAME

ARG POSTGRES_DB
ARG POSTGRES_PORT
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST

ARG DIGITAL_SPB_TOKEN

ARG REDIS_HOST
ARG REDIS_PORT
ARG REDIS_PASSWORD

ARG APP_PORT

ADD /docker/backend/create_env.sh /backend/
RUN /bin/sh /backend/create_env.sh > /etc/sysconfig/backend

ADD /docker/backend/backend.service /etc/systemd/system/
RUN set -ex \
    && systemctl enable backend.service

ADD /backend /backend

EXPOSE ${APP_PORT}