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
ARG API_DOC_PREFIX

ARG POSTGRES_DB
ARG POSTGRES_PORT
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST

ARG DIGITAL_SPB_TOKEN
ARG VK_CLIENT_SECRET

ARG REDIS_HOST
ARG REDIS_PORT
ARG REDIS_PASSWORD

ARG APP_PORT

ENV DEBUG=$DEBUG
ENV VERSION=$VERSION
ENV SERVER_NAME=$SERVER_NAME
ENV PROJECT_NAME=$PROJECT_NAME

ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_HOST=$POSTGRES_HOST

ENV DIGITAL_SPB_TOKEN=$DIGITAL_SPB_TOKEN
ENV VK_CLIENT_SECRET=$VK_CLIENT_SECRET
ENV REDIS_HOST=$REDIS_HOST
ENV REDIS_PORT=$REDIS_PORT
ENV REDIS_PASSWORD=$REDIS_PASSWORD

ENV APP_PORT=$APP_PORT
ENV API_DOC_PREFIX=$API_DOC_PREFIX

ADD /docker/backend/create_env.sh /backend/
RUN /bin/sh /backend/create_env.sh > /etc/sysconfig/backend

ADD /docker/backend/backend.service /etc/systemd/system/
RUN set -ex \
    && systemctl enable backend.service

ADD /backend /backend

EXPOSE ${APP_PORT}