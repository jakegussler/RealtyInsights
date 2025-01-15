import pandas as pd
import os
from dotenv import load_dotenv
from utils.logger_utils import setup_logging
from utils.file_utils import write_df_to_csv, prepare_and_clean_folder

load_dotenv()
logger = setup_logging()

COLUMN_MAPPING = {
    'S1903_C02_001E': 'median_income',
    'S1903_C02_001M': 'median_income_margin_of_error',
    'S1903_C02_001EA': 'median_income_annotation',
    'S1903_C02_001MA': 'median_income_margin_of_error_annotation',
    'S1903_C03_001E': 'median_income',
    'S1903_C03_001M': 'median_income_margin_of_error',
    'S1903_C03_001EA': 'median_income_annotation',
    'S1903_C03_001MA': 'median_income_margin_of_error_annotation',
    'B01003_001E': 'population',
    'B01003_001M': 'population_margin_of_error',
    'B01003_001EA': 'population_annotation',
    'B01003_001MA': 'population_margin_of_error_annotation',
    'S0101_C01_001E': 'population',
    'S0101_C01_001M': 'population_margin_of_error',
    'S0101_C01_001EA': 'population_annotation',
    'S0101_C01_001MA': 'population_margin_of_error_annotation',
    'S0101_C01_001E': 'population',
    'S0101_C01_001M': 'population_margin_of_error',
    'S0101_C01_001EA': 'population_annotation',
    'S0101_C01_001MA': 'population_margin_of_error_annotation'
}





def add_year_column(df, year: str) -> pd.DataFrame:
    """
    Process the data from the census API
    Parameters:
    df: The data to process
    year (str): The year to process
    """

    try:
        # Add year column to DataFrame
        logger.info(f"Adding year column to DataFrame")
        df['year'] = year
        return df
    except Exception as e:
        logger.error(f"Error adding year column for {year}")

def get_year_from_file_name(file_name: str) -> str:
    """
    Get the year from a filename
    Parameters:
    filename (str): The filename to extract the year from
    """
    try:
        return file_name.split('_')[2].split('.')[0]
    except Exception as e:
        logger.error(f"Error getting year from filename {file_name}: {e}")
        return None

def map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map the columns in a DataFrame
    Parameters:
    df (pd.DataFrame): The DataFrame to map columns for
    """
    try:
        # Log the columns being mapped
        mapped_columns = {col: COLUMN_MAPPING[col] for col in df.columns if col in COLUMN_MAPPING}
        logger.info(f"Columns being mapped: {mapped_columns}")

        return df.rename(columns=COLUMN_MAPPING)
    except Exception as e:
        logger.error(f"Error mapping columns: {e}")
        return df


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


def process_census_file(raw_file_path: str, processed_file_path: str) -> None:
    """
    Process a single census file
    Parameters:
    raw_file_pathh (str): The path to the raw file
    processed_file_path (str): The path to save the processed file   
    """

    logger.info(f"Processing file: {raw_file_path}")
    try:
        # Read the file and remove the state column
        df = pd.read_csv(raw_file_path)
        df = map_columns(df)
        df = add_year_column(df, get_year_from_file_name(raw_file_path))
        df = remove_column(df, 'state')

    except Exception as e:
        logger.error(f"Error processing file {raw_file_path}: {e}")
    try:
        # Save the processed data to a consolidated CSV file
        write_df_to_csv(df, processed_file_path, append=True)
    except Exception as e:
        logger.error(f"Error saving processed data to {processed_file_path}: {e}")



def process_and_consolidate_census_files(raw_folder_path: str, consolidated_file_path: str) -> None:
    """
    Process all the CSV files in a folder and consolidate them into a single CSV file
    Parameters:
    folderpath_raw (str): The path to the folder containing the raw files
    consolidated_file_path (str): The path to save the consolidated file
    """

    processed_folder_path = os.path.dirname(consolidated_file_path)
    prepare_and_clean_folder(processed_folder_path) 

    logger.info(f"Processing all files in {raw_folder_path}")
    for file in os.listdir(raw_folder_path):
        if file.endswith(".csv"):
            process_census_file(raw_file_path=os.path.join(raw_folder_path, file), processed_file_path=consolidated_file_path)


def main():

    project_path = os.getenv("PROJECT_PATH")
    census_raw_folder = os.path.join(project_path, 'data/raw/census')
    consolidated_file_path=os.path.join(project_path, 'data/processed/census/census_data.csv')

    logger.info(f"Processing census files in {census_raw_folder}")
    process_and_consolidate_census_files(raw_folder_path=census_raw_folder, consolidated_file_path=consolidated_file_path)


if __name__ == "__main__":
    main()