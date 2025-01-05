#!/bin/bash

#Get environment variables from .env file
ENV_FILE="${1:-../.env}"

if [ -f "$ENV_FILE" ]; then
    echo "Retrieving variables from $ENV_FILE"
    source "$ENV_FILE"
else
    echo ".env file not found in $ENV_FILE, exiting"
    exit 1
fi


export PGPASSWORD="${DB_SUPERUSER_PASSWORD}"


echo "Creating database ${DB_NAME}"

#Connect to postgres as super user and run commands
psql -U $DB_SUPERUSER -h $DB_HOST <<EOF

--Drop and create database
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE $DB_NAME;


EOF

unset PGPASSWORD
echo "database ${DB_NAME} created"