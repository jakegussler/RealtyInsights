import requests
from utils.logger_utils import setup_logging
import pandas as pd
from dotenv import load_dotenv
from utils.api_utils import get_response, get_response_as_df
from utils.file_utils import prepare_and_clean_folder, write_df_to_csv
import os


logger = setup_logging()
load_dotenv()

BASE_URL_TEMPLATE='https://api.census.gov/data/{year}/acs/acs5/subject'
FILE_NAME_TEMPLATE='census_data_{year}.csv'
DEFAULT_COLUMNS=['NAME', 'GEO_ID']
INCOME_COLUMNS = {
    '2016':'S1903_C02_001E,S1903_C02_001M,S1903_C02_001EA,S1903_C02_001MA',
    'DEFAULT':'S1903_C03_001E,S1903_C03_001M,S1903_C03_001EA,S1903_C03_001MA'
}
POPULATION_COLUMNS = {
    'DEFAULT':'S0101_C01_001E,S0101_C01_001M,S0101_C01_001EA,S0101_C01_001MA'
}

def get_column_string(year: str) -> str:
    # Get the columns for the year
    columns = ','.join([
        INCOME_COLUMNS.get(year, INCOME_COLUMNS['DEFAULT']),
        POPULATION_COLUMNS.get(year, POPULATION_COLUMNS['DEFAULT'])
    ])
    return ','.join(DEFAULT_COLUMNS + columns.split(','))


def get_census_json_data(year: str, params: dict):
    """
    Retrieve data from the Census API as JSON
    Parameters:
    year (str): The year to retrieve data for
    params (dict): dictionary of parameters to pass to the API
    """
    url = BASE_URL_TEMPLATE.format(year=year)
    try:
        response = get_response(url, params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting response for {year}: {e}")
        return None
    



def get_census_as_df(year) -> pd.DataFrame:
    """
    Retrieve data from the Census API
    Parameters:
    years (list): The years to retrieve data for
    """
    url = BASE_URL_TEMPLATE.format(year=year)
    params =  {
    'get': get_column_string(year),
    'for': 'zip code tabulation area:*'
    }

    logger.info(f"Downloading Census data for {year}: {params}")
    df = get_response_as_df(url, params)

    logger.info(f"Processed data for {year}")
    if df is not None:
        return df
    else:
        return None

def download_census_data(folderpath:str, first_year: int, last_year: int) -> None:
    """
    Download census data for a range of years and save to a Parquet file
    Parameters:
    filepath (str): The path to save the CSV file
    first_year (int): The first year to download data for
    last_year (int): The last year to download data for
    """

    # Create a list of years to download
    years = []
    for year in range(first_year, last_year+1):
        years.append(str(year))
    
    for year in years:
        # Create the file path
        filename = FILE_NAME_TEMPLATE.format(year=year)
        filepath = os.path.join(folderpath, filename)
        try:
            # Get data from the Census API
            df = get_census_as_df(year)
        except Exception as e:
            logger.error(f"Error getting data for {year}: {e}")
        try:
            if df is not None:
                # Write the data to a CSV
                write_df_to_csv(df, filepath=filepath, append=True)
            else:
                logger.error("Dataframe is None, skipping write to CSV")
        except Exception as e:
            logger.error(f"Error saving {year} data to {filepath}: {e}")



def main() -> None:

    folderpath = os.path.join(os.getenv("PROJECT_PATH"), 'data/raw/census')
    

    prepare_and_clean_folder(folderpath)

    download_census_data(folderpath=folderpath, first_year=2016, last_year=2023)


if __name__ == "__main__":
    main()
