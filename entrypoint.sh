#!/usr/bin/dumb-init /bin/sh
if [ ! -s config.py ]; then
    cat config_docker.py > config.py
fi
exec ./jms start all 
