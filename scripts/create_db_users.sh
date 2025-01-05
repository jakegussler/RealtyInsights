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
psql -U $DB_SUPERUSER -h $DB_HOST <<EOF

--Drop and create ingest user
DROP USER IF EXISTS ${DB_INGEST_USER};
CREATE USER ${DB_INGEST_USER} WITH PASSWORD '${DB_INGEST_PASSWORD}';

--Drop and create dbt user
DROP USER IF EXISTS ${DB_DBT_USER};
CREATE USER ${DB_DBT_USER} WITH PASSWORD '${DB_DBT_PASSWORD}';

--Grant privileges to user
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_INGEST_USER};
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_DBT_USER};

EOF

echo "users ${DB_INGEST_USER} and ${DB_DBT_USER} created"