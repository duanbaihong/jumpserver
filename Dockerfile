FROM alpine
MAINTAINER dbh888 <duanbaihong@qq.com>

ENV LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 VERSION=1.4.6 EXT_PACKAGE="python3 py3-pip dumb-init" EXT_TMP_PACKAGE="make gcc g++"
WORKDIR /opt/jumpserver
COPY . /opt/jumpserver
# ADD https://github.com/jumpserver/jumpserver/archive/${VERSION}.tar.gz /opt/jumpserver
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    # tar xvf ${VERSION}.tar.gz \
    # && mv jumpserver-${VERSION}/* . \
    # && rm -rf jumpserver-${VERSION} \
    && apk add --no-cache $(cat requirements/alpine_requirements.txt) ${EXT_PACKAGE} ${EXT_TMP_PACKAGE} \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements/requirements.txt \
    && apk del ${EXT_TMP_PACKAGE} \
    && rm -rf ~/.cache/pip　\
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && mkdir -p /opt/jumpserver/tmp

VOLUME ["/opt/jumpserver/data","/opt/jumpserver/logs"]

EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
