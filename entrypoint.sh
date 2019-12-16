#!/usr/bin/dumb-init /bin/sh
if [ ! -s config.yml ]; then
    cp -f config_example.yml config.yml
fi
exec ./jms start all 
