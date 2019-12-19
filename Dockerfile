FROM alpine:3.10.2
MAINTAINER dbh888 <duanbaihong@qq.com>

ENV LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 VERSION=1.4.6 EXT_PACKAGE="python3 py3-pip dumb-init sshpass" EXT_TMP_PACKAGE="make gcc g++ postgresql-dev mariadb-dev sqlite-dev libffi-dev tiff-dev jpeg-dev zlib-dev freetype-dev lcms-dev libwebp-dev tcl-dev tk-dev python3-dev libressl-dev openldap-dev cyrus-sasl-dev krb5-dev"

COPY . /opt/jumpserver
# ADD https://github.com/jumpserver/jumpserver/archive/${VERSION}.tar.gz /opt/jumpserver
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && mkdir -p /root/.config/pip/ \
    && echo -e "[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple\n[install]\ntrusted-host=mirrors.aliyun.com" >$HOME/.config/pip/pip.conf \
    && apk add --no-cache $(cat /opt/jumpserver/requirements/alpine_requirements.txt) ${EXT_PACKAGE} ${EXT_TMP_PACKAGE} \
    && pip3 install --upgrade pip \
    && pip3 install -r /opt/jumpserver/requirements/requirements.txt \
    && apk del ${EXT_TMP_PACKAGE} \
    && rm -rf Dockerfile ~/.cache/pip　.gitignore .dockerignore\
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && mkdir -p /opt/jumpserver/tmp

VOLUME ["/opt/jumpserver/data","/opt/jumpserver/logs"]

EXPOSE 8080

WORKDIR /opt/jumpserver

ENTRYPOINT ["./entrypoint.sh"]
