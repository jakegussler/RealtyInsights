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

cd ${PROJECT_PATH}

# Create a virtual environment and activate
python -m venv venv

source venv/bin/activate

# Windows
#source myenv/Scripts/activate

