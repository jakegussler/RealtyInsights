from sqlalchemy import create_engine
from utils.config import DB_CONFIG
from utils.logger_utils import setup_logging
from sqlalchemy import text
import pandas as pd

logger = setup_logging()

def get_engine():
    connection_string = f'{DB_CONFIG["type"]}://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}'
    return create_engine(connection_string)


def delete_table(schema: str, table_name: str) -> None:
    """
    Delete a table from the database
    Parameters:
    schema (str): The schema of the table to delete
    table_name (str): The name of the table to delete
    """

    engine = get_engine()
    try:
        with engine.connect() as connection:
            connection.execute(
                text('DROP TABLE IF EXISTS "{}"."{}" CASCADE'.format(schema, table_name))
            )
            connection.commit()
            logger.info(f"SQL Command: DROP TABLE IF EXISTS {schema}.{table_name} CASCADE")
    except Exception as e:
        logger.error(f"An error occurred while deleting table {table_name}: {str(e)}")
        raise
        

def create_table(df: pd.DataFrame, schema: str, table_name: str) -> None:
    """
    Create a table in the database with all columns as VARCHAR
    Parameters:
    df (pd.DataFrame): The DataFrame to use to create the table
    schema (str): The schema to create the table in
    table_name (str): The name of the table to create
    """

    engine = get_engine()
    columns_list = df.columns.tolist()

    #Create SQL Statement
    column_definitions = ", ".join([f'"{col}" VARCHAR' for col in columns_list])
    sql_statement = f'CREATE TABLE "{schema}"."{table_name}" ({column_definitions});'

    try:
        with engine.connect() as connection:
            connection.execute(text(sql_statement))
            connection.commit()
            logger.info(f"SQL Command: {sql_statement}")
    except Exception as e:
        logger.error(f"An error occurred while creating table {table_name}: {str(e)}")
        raise
