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

#Connect to postgres as super user and run commands
psql -U $DB_SUPERUSER -h $DB_HOST -d ${DB_NAME} <<EOF

--Grant privileges to ingest user
GRANT ALL PRIVILEGES ON SCHEMA raw_realtor TO ${DB_INGEST_USER};
GRANT ALL PRIVILEGES ON SCHEMA raw_census TO ${DB_INGEST_USER};


GRANT ALL PRIVILEGES ON SCHEMA stg_realtor, stg_census, intermediate, marts_realty_insights TO ${DB_DBT_USER};

