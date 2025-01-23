import pandas as pd
from dotenv import load_dotenv
import os
from utils.logger_utils import setup_logging
from utils.api_utils import get_response_as_df
from utils.file_utils import prepare_and_clean_folder, write_df_to_csv
from utils.census_utils2 import load_census_config, get_column_string

logger = setup_logging()
load_dotenv()

BASE_URL_TEMPLATE = 'https://api.census.gov/data/{year}/acs/acs5'
FILE_NAME_PREFIX = 'census_acs5'

def create_file_name(year: int, table_name: str=None) -> str:
    """Create a file name for the processed Census data."""
    if table_name is None:
        return f"{FILE_NAME_PREFIX}_base_zip_{year}.csv"
    return f"{FILE_NAME_PREFIX}_{table_name}_zip_{year}.csv"

def create_url(year: int, table: dict) -> str:
    """Create URL for Census API request."""
    if table['url_segment'] is None:
        return f"{BASE_URL_TEMPLATE.format(year=str(year))}"
    return f"{BASE_URL_TEMPLATE.format(year=str(year))}/{table['url_segment']}"

def get_census_as_df(config: dict, year: int, table: dict, variables: list) -> pd.DataFrame | None:
    """Retrieve data from the Census API for a specific year."""
    url = create_url(year, table)
    table_name = table['name']

    params = {
        'get': get_column_string(config, year, table_name, variables),
        'for': 'zip code tabulation area:*'
    }
    
    logger.info(f"Downloading Census data for {year}: {params}")
    
    try:
        df = get_response_as_df(url, params)
        logger.info(f"Processed data for {year}")
        return df
    except Exception as e:
        logger.error(f"Error getting data for {year}: {e}")
        return None

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

    for year in years:

        num_variables = len(config['variables'].get(table_name, []))
        # Split variables into chunks of 12 to avoid API column number limit
        chunk_size = 12
        num_chunks = (num_variables + chunk_size - 1) // chunk_size 

        for i in range(num_chunks):

            # Get variables for this chunk
            start = i * chunk_size
            end = min((i + 1) * chunk_size, num_variables)
            variables = list(config['variables'].get(table_name, []))[start:end]

            file_name = create_file_name(year, table_name)
            if i > 0:
                file_name = file_name.replace('.csv', f'_{i}.csv')
            file_path = os.path.join(folder_path, file_name)

            try:
                df = get_census_as_df(config, year, table, variables)
                if df is not None:
                    write_df_to_csv(df, file_path, append=True)
                else:
                    logger.error("Dataframe is None, skipping write to CSV")
            except Exception as e:
                logger.error(f"Error saving {year} data to {file_path}: {e}")

def main() -> None:
    # Load configuration
    config_path = os.path.join(
        os.getenv("PROJECT_PATH"),
        'config/census_variables.yml'
    )
    config = load_census_config(config_path)
    

    for table in config['tables']:

        # Set up folder
        folder_path = os.path.join(os.getenv("PROJECT_PATH"), 'data/raw/census', table['name'])
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