import pandas as pd
import os
import math
from typing import TypedDict
from utils.logger_utils import setup_logging
from utils.api_utils import get_response_as_df
from utils.file_utils import prepare_and_clean_folder, write_df_to_csv, get_project_path
from utils.census_utils import load_census_config, get_column_string

logger = setup_logging()

class CensusConfig(TypedDict):
    variables: dict[str, dict]
    suffixes: list[str]
    geo_levels: list[dict]
    default_columns: list[str]


def create_file_name(config: dict, year: int, chunk_number: int,geo_level: str, table_name: str=None) -> str:
    """Create a file name for the processed Census data."""
    file_name_prefix = config['constants']['file_name_prefix']

    return f"{file_name_prefix}_{table_name}_{geo_level}_{year}_{chunk_number}.csv"

def create_url(config: dict, year: int, table: dict) -> str:
    """Create URL for Census API request."""
    base_url_template = config['constants']['base_url_template']
    if table['url_segment'] is None:
        return f"{base_url_template.format(year=str(year))}"
    return f"{base_url_template.format(year=str(year))}/{table['url_segment']}"

def get_census_as_df(config: dict, year: int, table: dict, geo_level:dict, variables: list) -> pd.DataFrame | None:
    """Retrieve data from the Census API for a specific year."""
    url = create_url(config, year, table)
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

def calculate_chunk_variables(config: dict, table_name: str, chunk_index: int) -> list:
    """
    Calculate variables for a chunk accounting for suffixes multiplication.
    In the census data, each variable has multiple suffixes that represent different measures.
    The API allows for a maximum of 50 variables per request. This function calculates the
    variables for a chunk based on the number of suffixes and the total number of variables.
    """
    num_suffixes = len(config['suffixes'])
    num_default_columns = len(config['default_columns'])
    child_var_limit = 50
    parent_var_limit = (child_var_limit - num_default_columns) // num_suffixes
    
    variables = list(config['variables'].get(table_name, []))
    start = chunk_index * parent_var_limit
    end = min((chunk_index + 1) * parent_var_limit, len(variables))
    
    return variables[start:end]

def validate_year_range(first_year: int, last_year: int) -> None:
    if first_year > last_year:
        raise ValueError("First year must be less than or equal to last year")
    if first_year < 2000:  # Or whatever earliest valid year is
        raise ValueError("Census API data not available before 2000")

def download_census_data(
    folder_path: str,
    first_year: int,
    last_year: int,
    config: CensusConfig,
    table: dict
) -> None:
    """Download census data for a range of years and save to CSV files."""
    years = [year for year in range(first_year, last_year + 1)]
    table_name = table['name']

    for geo_level in config['geo_levels']:

        for year in years:

            num_chunks = calculate_num_chunks(config, table_name)
            for chunk_index in range(num_chunks):
                # Get variables for this chunk       
                variables = calculate_chunk_variables(config, table_name, chunk_index)
                logger.info(f"Downloading data for {year} chunk {chunk_index+1}/{num_chunks}\n")
                logger.debug(f"Variables: {variables}")

                file_name = create_file_name(config, year, chunk_index, geo_level['file_name_segment'], table_name)
                file_path = os.path.join(folder_path, file_name)

                try:
                    df = get_census_as_df(config, year, table, geo_level, variables)
                    if df is not None:
                        write_df_to_csv(df, file_path, append=True)
                    else:
                        logger.error("Dataframe is None, skipping write to CSV")
                except Exception as e:
                    logger.error(f"Error saving {year} data to {file_path}: {e}")

def validate_year_range(start_year: int, end_year: int) -> None:
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise ValueError("Year range must be integers")
    if start_year > end_year:
        raise ValueError("First year must be less than or equal to last year")
    if start_year < 2009:
        raise ValueError("Census American Community Survet 5-year API data not available before 2009")
    

def get_year_range(config: dict) -> tuple:
    """
    Get the year range from the configuration.
    Returns: tuple: The first and last year in the range"""
    try:
        start_year = config['constants']['year_range']['start']
        end_year = config['constants']['year_range']['end']
        validate_year_range(start_year, end_year)
    except KeyError as e:
        logger.error(f"Error getting year range from configuration, check if year_range exists with start and end values: {e}")
        raise


def main(project_path=None, config_path=None, config=None) -> None:
    if project_path is None:
        project_path = get_project_path()
    if config_path is None:
        config_path = os.path.join(project_path, 'config/census_variables.yml')
    if config is None:
        config = load_census_config(config_path)
    
    for table in config['tables']:
        folder_path = os.path.join(project_path, 'data/raw/census', table['name'])
        prepare_and_clean_folder(folder_path)
        download_census_data(
            folder_path=folder_path,
            first_year=config['constants']['first_year'],
            last_year=config['constants']['last_year'],
            config=config,
            table=table,
        )


if __name__ == "__main__":
    main()