import os
from dotenv import load_dotenv


load_dotenv()

DB_CONFIG = {
    'type': os.getenv('DB_TYPE'),
    'user': os.getenv('DB_INGEST_USER'),
    'password': os.getenv('DB_INGEST_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}


