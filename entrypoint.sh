#!/usr/bin/dumb-init /bin/sh

. init_jumpserver
formatOutput title

id ${JUMPSERVER_USER} &>/dev/null 2>&1
if [ $? -ne 0 ]; then
    formatOutput "Initial ${JUMPSERVER} User [\033[31m${JUMPSERVER_USER}\033[0m]"
    #statements
    adduser -D -h ${JUMPSERVER_INSTALL} -s /sbin/nologin ${JUMPSERVER_USER} >& /dev/null;
    printOK $?
    formatOutput "Repair work directory [${JUMPSERVER_INSTALL}] permissions...."
    chown ${JUMPSERVER_USER}.${JUMPSERVER_USER} .  -R
    printOK $?
fi
su-exec ${JUMPSERVER_USER}:${JUMPSERVER_USER} jms start all 
