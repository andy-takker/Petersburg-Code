FROM almalinux:9

ARG PYTHON_VERSION=3.10.7
ARG PYTHON_PACKAGE=Python-$PYTHON_VERSION

RUN dnf update -y && dnf install wget yum-utils make gcc openssl-devel bzip2-devel libffi-devel zlib-devel sqlite-devel -y
RUN wget "https://www.python.org/ftp/python/$PYTHON_VERSION/$PYTHON_PACKAGE.tgz" \
    && tar xzf "$PYTHON_PACKAGE.tgz"
RUN cd "$PYTHON_PACKAGE"  \
    && ./configure --with-system-ffi --with-computed-gotos --enable-loadable-sqlite-extensions  \
    && make  \
    && make altinstall

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

ADD /docker/backend/create_env.sh /backend/
RUN /bin/sh /backend/create_env.sh > /etc/sysconfig/backend

ADD /docker/backend/backend.service /etc/systemd/system/
RUN set -ex \
    && systemctl enable backend.service

ADD /backend /backend

EXPOSE ${APP_PORT}