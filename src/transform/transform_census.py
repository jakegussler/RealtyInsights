import pandas as pd
import os
from dotenv import load_dotenv
from utils.logger_utils import setup_logging
from utils.file_utils import write_df_to_csv, create_output_dir, delete_csv

load_dotenv()
logger = setup_logging()

def remove_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Remove a column from a DataFrame
    Parameters:
    df (pd.DataFrame): The DataFrame to remove the column from
    column (str): The name of the column to remove
    """
    try:
        if column in df.columns:
            logger.info(f"Removing column: {column}")
            return df.drop(columns=[column])
        else:
            logger.info(f"Column {column} not found in DataFrame")
            return df
    except Exception as e:
        logger.error(f"Error removing column {column}: {e}")
        return df


def process_census_file(filepath_raw: str, filepath_processed: str) -> None:
    """
    Process a single census file
    Parameters:
    filepath_raw (str): The path to the raw file
    filepath_processed (str): The path to save the processed file
    """

    logger.info(f"Processing file: {filepath_raw}")
    try:
        # Read the file and remove the state column
        df = pd.read_csv(filepath_raw)
        df = remove_column(df, 'state')
    except Exception as e:
        logger.error(f"Error processing file {filepath_raw}: {e}")
    try:
        # Save the processed data to a consolidated CSV file
        write_df_to_csv(df, filepath_processed, append=True)
    except Exception as e:
        logger.error(f"Error saving processed data to {filepath_processed}: {e}")

def prepare_processed_folder(folderpath: str) -> None:
    """
    Prepare the processed folder by creating output directory
    then deleting any existing files if output directory exists
    Parameters:
    folderpath (str): The path to the folder to prepare
    """
    try:
        create_output_dir(folderpath)
        delete_csv(os.path.join(folderpath, 'census_data.csv'))
    except Exception as e:
        logger.error(f"Error preparing folder {folderpath}: {e}")

def process_all_census_files(folderpath_raw: str, folderpath_processed: str) -> None:
    """
    Process all the CSV files in a folder
    Parameters:
    folderpath_raw (str): The path to the folder containing the raw files
    folderpath_processed (str): The path to the folder to save the processed files
    """
    prepare_processed_folder(folderpath_processed)
    filepath_processed = os.path.join(folderpath_processed, 'census_income_zip.csv')

    logger.info(f"Processing all files in {folderpath_raw}")
    for file in os.listdir(folderpath_raw):
        if file.endswith(".csv"):
            process_census_file(os.path.join(folderpath_raw, file), filepath_processed)


def main():

    project_path = os.getenv("PROJECT_PATH")
    census_raw_folder = os.path.join(project_path, 'data/raw/census')
    census_processed_folder = os.path.join(project_path, 'data/processed/census')

    process_all_census_files(census_raw_folder, census_processed_folder)


if __name__ == "__main__":
    main()