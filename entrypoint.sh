#!/usr/bin/dumb-init /bin/sh
. init_jumpserver
formatOutput title
if [ ! -s config.yml ]; then
    formatOutput "Fix File Permissions...."
    chown root.root . -R
    printOK $?
    formatOutput "Generate configuration file config.yml...."
    cat config_example.yml > config.yml
    printOK $?
fi
sleep 240
exec ./jms start all 
