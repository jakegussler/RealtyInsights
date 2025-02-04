#!/bin/bash

#Get variables from .env file
ENV_FILE="${1:-../.env}"

if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "can not find .env file in $ENV_FILE, exiting..."
    return 1
fi


#Set password for postgresql
export PGPASSWORD="${DB_SUPERUSER_PASSWORD}"

#Connect to postgres as super user and run commands
psql -U ${DB_SUPERUSER} -h $DB_HOST -d $DB_NAME -w <<EOF

CREATE SCHEMA IF NOT EXISTS raw_realtor;
CREATE SCHEMA IF NOT EXISTS raw_census;
CREATE SCHEMA IF NOT EXISTS stg_realtor;
CREATE SCHEMA IF NOT EXISTS stg_census;
CREATE SCHEMA IF NOT EXISTS intermediate;
CREATE SCHEMA IF NOT EXISTS marts_realty_insights;



EOF

echo "Schema creation completed"
