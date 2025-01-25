import pandas as pd
from dotenv import load_dotenv
import os
import math
from pathlib import Path
from utils.logger_utils import setup_logging
from utils.api_utils import get_respon e_as_df
from utils.file_utils import prepare_and_clean_folder, write_df_to_csv, get_project_path
from utils.census_utils import load_census_config, get_column_string

logger = setup_logging()
load_dotenv()

BASE_URL_TEMPLATE = 'https://api.census.gov/data/{year}/acs/acs5'
FILE_NAME_PREFIX = 'census_acs5'

def create_file_name(year: int, chunk_number: int,geo_level: str, table_name: str=None) -> str:
    """Create a file name for the processed Census data."""
    if table_name is None:
        return f"{FILE_NAME_PREFIX}_base_zip_{year}_{chunk_number}.csv"
    return f"{FILE_NAME_PREFIX}_{table_name}_{geo_level}_{year}_{chunk_number}.csv"

def create_url(year: int, table: dict) -> str:
    """Create URL for Census API request."""
    if table['url_segment'] is None:
        return f"{BASE_URL_TEMPLATE.format(year=str(year))}"
    return f"{BASE_URL_TEMPLATE.format(year=str(year))}/{table['url_segment']}"

def get_census_as_df(config: dict, year: int, table: dict, geo_level:dict, variables: list) -> pd.DataFrame | None:
    """Retrieve data from the Census API for a specific year."""
    url = create_url(year, table)
    table_name = table['name']

    params = {
        'get': get_column_string(config, year, table_name, variables),
        'for': f'{geo_level['for_parameter']}:*'
    }
    
    logger.info(f"Downloading Census data for {year}: {params}")
    
    try:
        df = get_response_as_df(url, params)
        logger.info(f"Processed data for {year}")
        return df
    except Exception as e:
        logger.error(f"Error getting data for {year}: {e}")
        return None

def calculate_chunk_size(config: dict, table_name: str) -> int:
    """Calculate the chunk size for Census API requests."""
    num_variables = len(config['variables'].get(table_name, []))
    return math.floor(50 / len(config['suffixes']))

def calculate_num_chunks(config: dict, table_name: str) -> int:
    """Calculate the number of chunks for Census API requests."""
    num_variables = len(config['variables'].get(table_name, []))
    chunk_size = calculate_chunk_size(config, table_name)
    return (num_variables + chunk_size - 1) // chunk_size

def download_census_data(
    folder_path: str,
    first_year: int,
    last_year: int,
    config: dict,
    table: dict
) -> None:
    """Download census data for a range of years and save to CSV files."""
    years = [year for year in range(first_year, last_year + 1)]
    table_name = table['name']

    for geo_level in config['geo_levels']:

        for year in years:

            num_variables = sum(
                not var.get('overrides', {}).get(year, {}).get('missing', False)
                for var in config['variables'].get(table_name, []).values()
            )
            # Split variables into chunks by dividing max number of variables by number of suffixes
            chunk_size = math.floor(50 / len(config['suffixes']))
            num_chunks = calculate_num_chunks(config, table_name)

            for i in range(num_chunks):

                # Get variables for this chunk
                start = i * chunk_size
                end = min((i + 1) * chunk_size, num_variables)
                variables = list(config['variables'].get(table_name, []))[start:end - 1]
                logger.info(f"Downloading data for {year} chunk {i+1}/{num_chunks}\n")
                logger.debug(f"Variables: {variables}")

                file_name = create_file_name(year, i, geo_level['file_name_segment'], table_name)
                file_path = os.path.join(folder_path, file_name)

                try:
                    df = get_census_as_df(config, year, table, geo_level, variables)
                    if df is not None:
                        write_df_to_csv(df, file_path, append=True)
                    else:
                        logger.error("Dataframe is None, skipping write to CSV")
                except Exception as e:
                    logger.error(f"Error saving {year} data to {file_path}: {e}")

def main() -> None:

    project_path = get_project_path()
    # Load configuration using project path and config file path
    config_path = os.path.join(
        project_path,
        'config/census_variables.yml'
    )
    config = load_census_config(config_path)
    

    for table in config['tables']:

        # Set up folder
        folder_path = os.path.join(project_path, 'data/raw/census', table['name'])
        prepare_and_clean_folder(folder_path)
        
        # Download data
        download_census_data(
            folder_path=folder_path,
            first_year=2016,
            last_year=2023,
            config=config,
            table=table,
        )
    


if __name__ == "__main__":
    main()