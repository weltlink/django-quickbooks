#!/usr/bin/env bash

echo "################################## Run nginx"
export DOLLAR='$'
envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf
nginx -g "daemon off;"
