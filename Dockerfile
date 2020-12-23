# 拉取python镜像作为基本环境
#FROM postgres:latest
# 拉取python镜像作为基本环境
FROM sameersbn/postgresql
MAINTAINER "mathskiller" <chennuo909@163.com>

#FROM python:3.6.5
#FROM python:3.6-slim
#FROM python:3.6-alpine
# 将本地目录拷贝到container并且设置为工作目录
#ADD . /usr/src/bookstore
#WORKDIR /usr/src/bookstore
ADD . /home/bookstore
#WORKDIR /home/bookstore
COPY requirements.txt /home/bookstore
# 在container中运行命令
# install Python 3
#RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update && apt-get install -y python3 python3-pip
#RUN apt-get -y install python3.7-dev
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install python-dev python3-dev libxml2-dev libxslt1-dev zlib1g-dev gcc libpq-dev
# musl-dev postgresql-server-dev-10 postgresql-client-10
#RUN apt-get install -y postgresql-server-dev-10 gcc python3-dev musl-dev
# install requirements with PIP
RUN pip3 install -r /home/bookstore/requirements.txt


#RUN    /etc/init.d/postgresql start
#COPY *.sql /docker-entrypoint-initdb.d/
#ENV POSTGRES_USER=postgres


# 将flask 5001 postgres 5432 端口暴露出来
EXPOSE 5001
EXPOSE 5432
#RUN psql -c 'create database bookstore;' -U postgres
#RUN psql -c "ALTER USER postgres WITH PASSWORD '';" -U postgres
#CMD "/bin/bash"
# 容器启动的执行命令
#CMD export PYTHONPATH=$PYTHONPATH:$(pwd) \
#python ./initialize_database/initialize_books.py \
#&& python ./initialize_database/initialize_database.py \
#&& python ./initialize_database/initialize_search_database.py
