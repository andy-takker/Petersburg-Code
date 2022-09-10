#!/bin/sh
echo
if $DEBUG; then
  file="nginx.dev.conf"
else
  file="nginx.prod.conf"
fi
echo "DEBUG: ${DEBUG}" >> "/conf/test"
cp "/conf/${file}" /etc/nginx/conf.d/nginx.conf