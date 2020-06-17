FROM alpine:3.10.2
MAINTAINER dbh888 <duanbaihong@qq.com>
ARG JUMPSERVER_INSTALL=/opt/jumpserver
ENV LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 VERSION=1.4.6 \
	EXT_PACKAGE="python3 py3-pip su-exec dumb-init sshpass libldap openssh-client\
                krb5-libs mariadb-connector-c libjpeg tiff cyrus-sasl \
                freetype liblcms libwebp tcl xorgproto libuuid fontconfig \
                libblkid libfdisk libmount libxft libxrender libxcb libxdmcp libxau libxslt" \
    DEP_PACKAGE='jpeg-dev zlib-dev freetype-dev lcms-dev libwebp-dev \
                tcl-dev tk-dev python3-dev libressl-dev openldap-dev cyrus-sasl-dev krb5-dev \
                postgresql-dev mariadb-dev sqlite-dev libffi-dev gcc libc-dev \
                linux-headers make autoconf g++ libxslt-dev libxml2-dev' \
    JUMPSERVER_USER=jumpserver \
    JUMPSERVER_INSTALL=${JUMPSERVER_INSTALL} \
    PATH=${JUMPSERVER_INSTALL}:$PATH \
    PS1='[\u@\w]$'
COPY . /opt/jumpserver
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && mkdir -p /root/.config/pip/ \
    && echo -e "[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple\n[install]\ntrusted-host=mirrors.aliyun.com" >$HOME/.config/pip/pip.conf \
    && apk add --no-cache ${EXT_PACKAGE} ${DEP_PACKAGE} \
    && pip3 install --upgrade pip wheel \
    && pip3 install -r /opt/jumpserver/requirements/requirements.txt \
    && apk del ${DEP_PACKAGE} \
    && pip3 uninstall wheel \
    && rm -rf ~/.cache ${JUMPSERVER_INSTALL}/requirements \
    && ln -sf /usr/bin/python3 /usr/bin/python 

VOLUME ["${JUMPSERVER_INSTALL}/data","${JUMPSERVER_INSTALL}/logs","${JUMPSERVER_INSTALL}/conf"]

EXPOSE 8080 8070 5555

WORKDIR ${JUMPSERVER_INSTALL}

ENTRYPOINT ["./entrypoint.sh"]
