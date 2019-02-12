#!/usr/bin/dumb-init /bin/sh
if [ ! -s config.yml ]; then
    cp -f config_docker.yml config.yml
fi
exec ./jms start all 
