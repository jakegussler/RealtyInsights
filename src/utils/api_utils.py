import requests
from utils.logger_utils import setup_logging
import time

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