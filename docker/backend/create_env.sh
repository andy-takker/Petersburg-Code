#!/bin/sh
cat << EOF
DEBUG=${DEBUG}
PROJECT_NAME=${PROJECT_NAME}
SERVER_NAME=${SERVER_NAME}
VERSION=${VERSION}
APP_PORT=${APP_PORT}

POSTGRES_HOST=${POSTGRES_HOST}
POSTGRES_PORT=${POSTGRES_PORT}
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

REDIS_HOST=${REDIS_HOST}
REDIS_PORT=${REDIS_PORT}
REDIS_PASSWORD=${REDIS_PASSWORD}

DIGITAL_SPB_TOKEN=${DIGITAL_SPB_TOKEN}
VK_CLIENT_SECRET=${VK_CLIENT_SECRET}

API_DOC_PREFIX=${API_DOC_PREFIX}
EOF