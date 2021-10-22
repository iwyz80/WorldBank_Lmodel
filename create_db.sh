#!/bin/bash

set -e

read -p "Enter Database username: " DB_USER
read -sp "Enter Password: " DB_USER_PASS
echo
read -p "Enter Database name: " DB_NAME

echo DB_USER=$DB_USER >.env
echo DB_USER_PASS=$DB_USER_PASS >>.env
echo DB_NAME=$DB_NAME >>.env


sudo su postgres <<EOF
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_USER_PASS';"
psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER;"
psql -c "grant all privileges on database $DB_NAME to $DB_USER;"
echo "Postgres User '$DB_USER' and database '$DB_NAME' created."
EOF
