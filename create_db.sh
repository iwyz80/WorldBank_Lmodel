#!/bin/bash

set -e

DB_NAME=${1:-mudano_testdb}
DB_USER=${2:-mudano0710}
DB_USER_PASS=${3:-mudano0710}

sudo su postgres <<EOF
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_USER_PASS';"
psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER;"
psql -c "grant all privileges on database $DB_NAME to $DB_USER;"
echo "Postgres User '$DB_USER' and database '$DB_NAME' created."
EOF
