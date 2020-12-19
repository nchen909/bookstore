#!/usr/bin/env bash

set -ex

echo "Installing Postgres 10"
sudo find / -name 'postmaster.pid'  2>&1 | grep -v "Permission denied"
sudo service postgresql stop
#sudo find / -name 'postmaster.pid'  2>&1 | grep -v "Permission denied"
#sudo rm /var/ramfs/postgresql/9.6/main/postmaster.pid
sudo apt-get remove -q 'postgresql-*'
sudo apt-get update -q
sudo apt-get install -q postgresql-10 postgresql-client-10
sudo cp /etc/postgresql/{9.6,10}/main/pg_hba.conf

echo "Restarting Postgres 10"
sudo service postgresql restart
#sudo find / -name 'postmaster.pid'  2>&1 | grep -v "Permission denied"
#sudo rm /var/ramfs/postgresql/9.6/main/postmaster.pid
sudo pg_ctl -D /var/ramfs/postgresql/9.6/main -l /var/ramfs/postgresql/9.6/main/server.log start
sudo cat /var/ramfs/postgresql/9.6/main/server.log
sudo psql -c 'CREATE ROLE travis SUPERUSER LOGIN CREATEDB;' -U postgres
sudo psql -c 'create database bookstore;' -U postgres