import os
from dotenv import load_dotenv


load_dotenv()

DB_CONFIG = {
    'type': os.getenv('DB_TYPE', 'postgresql'),
    'user': os.getenv('DB_INGEST_USER', 'DB_INGEST_USER'),
    'password': os.getenv('DB_INGEST_PASSWORD', 'DB_INGEST_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'zillow_analytics')
}

API_CONFIG = {
    
}