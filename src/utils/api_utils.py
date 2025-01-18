import requests
from utils.logger_utils import setup_logging
import time
import pandas as pd

logger = setup_logging()

def get_response(url, params=None, max_retries=10, retry_delay=5, timeout=30):

    #Initial retry delay
    initial_retry_delay = retry_delay

    #Retry loop
    for attempt in range(max_retries):
        try:
            #Make the request to the API
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status() #Raise an error for bad HTTP responses
            #Exit attempt loop if successful
            if response.status_code == 200:
                #Reset the retry delay
                retry_delay = initial_retry_delay
                return response
        
        except requests.exceptions.RequestException as e:
            logger.info(f'Attempt {attempt + 1} of {max_retries} failed: {str(e)}')
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                
                #Exponential backoff
                if attempt > 0:
                    retry_delay = round(retry_delay * 1.5, 0)
                
                #Wait for the retry delay
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Returning None")
                return None
            
def get_response_as_json(url: str, params: dict):
    """
    Retrieve data from an API as JSON
    year (str): The year to retrieve data for
    params (dict): dictionary of parameters to pass to the API
    """
    try:
        response = get_response(url, params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting response for {url}: {e}")
        return None

def convert_json_to_df(data: list) -> None:
    """
    Process the data from the census API
    Parameters:
    data (list): The data to process
    """
    try:
        # Convert to dataframe
        logger.info(f"Converting response to DataFrame")
        df = pd.DataFrame(data[1:],columns=data[0])
        return df
    except Exception as e: 
        logger.error(f"Error converting to Dataframe {e}")
        return None


def get_response_as_df(url, params: dict) -> pd.DataFrame:
    """
    Retrieves data from an API and converts it to a DataFrame
    """
    logger.info(f"Downloading Data for {url}")
    data = get_response_as_json(url, params=params)

    if data is None:
        logger.error(f"No data received from {url}")
        return None
            
    if data:
        logger.info(f"Downloaded data for {url}")
        logger.debug(f"Data structure type: {type(data)}")
        logger.debug(f"First few elements: {data[:2] if isinstance(data, list) else data}")
        
        #Process the data as a DataFrame
        df = convert_json_to_df(data)

        if df is None:
            logger.error(f"Failed to convert data to DataFrame for {url}")
            return None
            
        logger.info(f"Processed data for {url}")
        return df

