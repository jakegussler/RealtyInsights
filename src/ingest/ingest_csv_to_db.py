import pandas as pd
import os
import datetime
from dotenv import load_dotenv
from utils.db_utils import get_engine, delete_table, create_table
from utils.logger_utils import setup_logging
from utils.file_utils import get_project_path


logger = setup_logging()
load_dotenv()

env = os.getenv("ENV")

def ingest_csv_to_db(file_path: str, schema: str, table_name: str) -> None:

    """
    Ingest the data from a CSV file into a PostgreSQL database

    Parameters:
    file_path (str): The path to the CSV file
    schema (str): The schema to ingest the data into
    table_name (str): The name of the table_name to ingest the data into

    """

    #Database connection
    engine = get_engine()
    chunksize = 1000
    max_retries = 10


    ingest_start_time = datetime.datetime.now()
 
    for chunk_number, chunk in enumerate(pd.read_csv(file_path, chunksize=chunksize)):
        for attempt in range(max_retries):  
            try:
                ingest_df_to_db(df=chunk,schema=schema, table_name=table_name, engine=engine)
                logger.info(f"Chunk number {chunk_number + 1} succesfully ingested into table {table_name}")
                break
            except Exception as e:
                logger.error(f"Error processing chunk {chunk_number}. Attempt {attempt + 1} of {max_retries}")
                if not (attempt < max_retries):
                    logger.error(f"Maximum number of attempts reached for chunk {chunk_number}")
                

    ingest_end_time = datetime.datetime.now()
    logger.info(f"Ingestion start time: {ingest_start_time}")
    logger.info(f"Ingestion end time: {ingest_end_time}")
    logger.info(f"Total ingestion time: {ingest_end_time - ingest_start_time}")



def ingest_df_to_db(df, schema: str, table_name: str, engine) -> None:
    """
    Ingest a DataFrame into a database
    Parameters:
    df (pd.DataFrame): The DataFrame to ingest
    schema (str): The schema to ingest to in the database
    table_name (str): The name of the table to ingest the data into
    engine (sqlalchemy.engine.base.Engine): The database engine to use
    """

    try:
        #Ingest the data into the database
        df.to_sql(table_name, engine, if_exists='append', schema=schema, index=False)
    except Exception as e:
        logger.error(f"An error occured while ingesting data into {table_name}: {str(e)}")
        raise

def ingest_all_csv_files_in_folder(folder_path: str, schema: str) -> None:
    """
    Ingest the Zillow CSV files into the PostgreSQL database
    Parameters:
    folder_path (str): The path to the folder containing the Zillow CSV files
    schema (str): The schema to ingest to in the database
    """

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = f"{folder_path}/{file}"
            table_name = file.split('.')[0].lower()
                
            #Prepare the database
            delete_table(schema="census_raw", table_name="census_data")
            create_table(df=pd.read_csv(file_path, nrows=1), schema=schema, table_name=table_name)

            ingest_csv_to_db(file_path=file_path, schema=schema, table_name=table_name)


def ingest_census_data(folder_path: str=None) -> None:
    """
    Ingest the processed census data into the database
    """

    
    if folder_path is None:
        #Get the file path
        project_path = get_project_path()
        folder_path = f"{project_path}/data/processed/census"
    
    ingest_all_csv_files_in_folder(folder_path=folder_path, schema="raw_census")

def ingest_realtor_data(folder_path: str=None) -> None:
    """
    Ingest the processed realtor data into the database
    """

    if folder_path is None:
        #Get the file path
        project_path = get_project_path()
        folder_path = f"{project_path}/data/raw/realtor"
    
    ingest_all_csv_files_in_folder(folder_path=folder_path, schema="raw_realtor")



def main():
    logger.info("Ingesting data into the database")
    #ingest_census_data()

if __name__ == "__main__":
    main()

