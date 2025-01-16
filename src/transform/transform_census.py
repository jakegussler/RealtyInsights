import pandas as pd
import os
from dotenv import load_dotenv
from utils.logger_utils import setup_logging
from utils.file_utils import write_df_to_csv, prepare_and_clean_folder
from utils.census_utils import load_census_config, create_column_mapping

load_dotenv()
logger = setup_logging()

def add_year_column(df: pd.DataFrame, year: str) -> pd.DataFrame:
    """Add year column to DataFrame."""
    try:
        logger.info("Adding year column to DataFrame")
        df['year'] = year
        return df
    except Exception as e:
        logger.error(f"Error adding year column for {year}: {e}")
        return df

def get_year_from_file_name(file_name: str) -> str:
    """Extract year from filename."""
    try:
        return file_name.split('censusdata')[-1].split('.')[0]
    except Exception as e:
        logger.error(f"Error getting year from filename {file_name}: {e}")
        return None

def map_columns(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """Map DataFrame columns using configuration."""
    try:
        # Get the intersection of DataFrame columns and mapping keys
        columns_to_map = {
            col: column_mapping[col] 
            for col in df.columns 
            if col in column_mapping
        }
        logger.info(f"Mapping columns: {columns_to_map}")
        return df.rename(columns=columns_to_map)
    except Exception as e:
        logger.error(f"Error mapping columns: {e}")
        return df

def remove_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Remove specified column from DataFrame."""
    try:
        if column in df.columns:
            logger.info(f"Removing column: {column}")
            return df.drop(columns=[column])
        logger.info(f"Column {column} not found in DataFrame")
        return df
    except Exception as e:
        logger.error(f"Error removing column {column}: {e}")
        return df

def process_census_file(
    raw_file_path: str,
    processed_file_path: str,
    column_mapping: dict
) -> None:
    """Process a single census file."""
    logger.info(f"Processing file: {raw_file_path}")
    try:
        # Read and transform the file
        df = pd.read_csv(raw_file_path)
        df = map_columns(df, column_mapping)
        df = add_year_column(df, get_year_from_file_name(raw_file_path))
        df = remove_column(df, 'state')

        # Save the processed data
        write_df_to_csv(df, processed_file_path, append=True)
    except Exception as e:
        logger.error(f"Error processing file {raw_file_path}: {e}")

def process_and_consolidate_census_files(
    raw_folder_path: str,
    consolidated_file_path: str,
    column_mapping: dict
) -> None:
    """Process all census files and consolidate into single file."""
    processed_folder_path = os.path.dirname(consolidated_file_path)
    prepare_and_clean_folder(processed_folder_path)

    logger.info(f"Processing all files in {raw_folder_path}")
    for file in os.listdir(raw_folder_path):
        if file.endswith(".csv"):
            process_census_file(
                raw_file_path=os.path.join(raw_folder_path, file),
                processed_file_path=consolidated_file_path,
                column_mapping=column_mapping
            )

def main() -> None:
    # Load paths from environment
    project_path = os.getenv("PROJECT_PATH")
    census_raw_folder = os.path.join(project_path, 'data/raw/census')
    consolidated_file_path = os.path.join(
        project_path,
        'data/processed/census/census_data.csv'
    )
    config_path = os.path.join(project_path, 'config/census_variables.yml')

    # Load configuration and create column mapping
    config = load_census_config(config_path)
    column_mapping = create_column_mapping(config)

    # Process files
    logger.info(f"Processing census files in {census_raw_folder}")
    process_and_consolidate_census_files(
        raw_folder_path=census_raw_folder,
        consolidated_file_path=consolidated_file_path,
        column_mapping=column_mapping
    )

if __name__ == "__main__":
    main()