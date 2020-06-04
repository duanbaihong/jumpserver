#!/bin/bash
#

version=$1
if [ -z "$version" ];then
    echo "Usage: sh build version"
    exit
fi


docker build -t 192.168.99.20/library/jumpserver:$version .
