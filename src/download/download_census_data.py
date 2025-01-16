import pandas as pd
from dotenv import load_dotenv
import os
from utils.logger_utils import setup_logging
from utils.api_utils import get_response_as_df
from utils.file_utils import prepare_and_clean_folder, write_df_to_csv
from utils.census_utils import load_census_config, get_column_string

logger = setup_logging()
load_dotenv()

BASE_URL_TEMPLATE = 'https://api.census.gov/data/{year}/acs/acs5/subject'
FILE_NAME_TEMPLATE = 'census_acs5_zip_{year}.csv'

def get_census_as_df(year: int, config: dict) -> pd.DataFrame | None:
    """Retrieve data from the Census API for a specific year."""
    url = BASE_URL_TEMPLATE.format(year=str(year))
    params = {
        'get': get_column_string(config, year),
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
    config: dict
) -> None:
    """Download census data for a range of years and save to CSV files."""
    years = [year for year in range(first_year, last_year + 1)]
    
    for year in years:
        file_name = FILE_NAME_TEMPLATE.format(year=str(year))
        file_path = os.path.join(folder_path, file_name)
        
        try:
            df = get_census_as_df(year, config)
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
    
    # Set up folder
    folder_path = os.path.join(os.getenv("PROJECT_PATH"), 'data/raw/census')
    prepare_and_clean_folder(folder_path)
    
    # Download data
    download_census_data(
        folder_path=folder_path,
        first_year=2016,
        last_year=2023,
        config=config
    )

if __name__ == "__main__":
    main()