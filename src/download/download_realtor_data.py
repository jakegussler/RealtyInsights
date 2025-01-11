from dotenv import load_dotenv
import os
import datetime
import time
from utils.logger_utils import setup_logging
import requests
from utils.file_utils import create_output_dir


#Load the environment variables
load_dotenv()

logger = setup_logging()

timestamps = {
    "start_time": None,
    "download_end_time": None,
    "write_end_time": None
    
}

def get_csv(url: str, csv_output_name: str, folderpath: str) -> None:

    """
    Make a request to download a CSV file
    """

    logger.info(f"Downloading {csv_output_name} from {url}...")
    

    timestamps["start_time"] = datetime.datetime.now()
    logger.info(f"Download start time: {timestamps['start_time']}")

    try:

        create_output_dir(folderpath=folderpath)

        response = get_response(url=url)
        if(response):
            
            timestamps["download_end_time"] = datetime.datetime.now()
            logger.info(f"Download end time: {timestamps["download_end_time"]}")
            
            filepath = f"{folderpath}/{csv_output_name}"

            write_response_to_csv(response=response, filepath=filepath)
            
            timestamps["write_end_time"] = datetime.datetime.now()
            logger.info(f"Download complete for {csv_output_name}, saved to {filepath}")
            logger.info(f"Time to download and process: {timestamps["write_end_time"] - timestamps["start_time"]}")

            
    except Exception as e:
        logger.error(f"Error getting response for {csv_output_name}: {e}")



def write_response_to_csv(response, filepath):

    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def get_response(url, url_parameters=None, max_retries=10, retry_delay=5, timeout=30):

    #Initial retry delay
    initial_retry_delay = retry_delay

    #Retry loop
    for attempt in range(max_retries):
        try:
            #Make the request to the API
            response = requests.get(url, params=url_parameters, timeout=timeout)
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

def download_all_realtor_csv_files(folderpath: str) -> None:
    
    """
    Download the Realtor.com CSV files
    
    Parameters:
    folderpath (str): The folder path to save the CSV files
    """

    base_url = 'https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/RDC_Inventory_Core_Metrics_'
    tables = ['Country', 'State', 'Metro', 'County', 'Zip']
    table_type = 'History'
    file_extension = '.csv'
    
    #Iterate through the tables
    for table in tables:
        url = base_url + table + "_" + table_type + file_extension
        csv_output_name = "realtor_" + table.lower() + ".csv"

        #Get the data from the API
        get_csv(url=url, csv_output_name=csv_output_name, folderpath=folderpath)

def main() -> None:

    folderpath = "/Users/jakegussler/Projects/RealtyInsights/data/raw/realtor"

    #Download the zillow tables
    download_all_realtor_csv_files(folderpath)

if __name__ == "__main__":
    main()


    

