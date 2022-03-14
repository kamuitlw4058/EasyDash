
FROM python:3

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY ./requirements.txt /easy_dash/requirements.txt
COPY ./setup.py /easy_dash/

COPY ./easy_dash /easy_dash/easy_dash
COPY ./apps /easy_dash/apps

# RUN  ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone && yum -y install wget && yum -y install lsof && yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel readline-devel tk-devel xz-devel libffi-devel && yum -y groupinstall "Development tools" && yum -y install java-1.8.0-openjdk.x86_64 && yum clean all && cd /usr/local/src/ && tar xvf Python-3.8.0.tar.xz && mv Python-3.8.0 /usr/local/python-3.8 && rm -f Python-3.8.0.tar.xz && cd /usr/local/python-3.8/ && ./configure --prefix=/usr/local/sbin/python-3.8 && make && make install && rm -rf /usr/bin/python && ln -sv /usr/local/sbin/python-3.8/bin/python3 /usr/bin/python && ln -sv /usr/local/sbin/python-3.8/bin/python3 /usr/bin/python3 && ln -sv /usr/local/sbin/python-3.8/bin/python3 /usr/bin/python38 && sed -i 1s/python/python2.7/ /usr/bin/yum && sed -i 1s/python/python2.7/ /usr/libexec/urlgrabber-ext-down && sed -i 1s/python/python2.7/ /usr/bin/yum-config-manager && sed -i '$a\JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk.x86_64' /etc/profile && sed -i '$a\PATH=$PATH:$JAVA_HOME/bin' /etc/profile && sed -i '$a\CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar' /etc/profile && sed -i '$a\export JAVA_HOME CLASSPATH PATH' /etc/profile && source /etc/profile && ln -s /usr/local/sbin/python-3.8/bin/pip3 /usr/bin/pip && pip install --upgrade pip


RUN cd easy_dash && python setup.py install && python -m pip install --upgrade pip &&\
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD ["bash"]





