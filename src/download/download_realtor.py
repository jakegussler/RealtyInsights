from dotenv import load_dotenv
import os
import datetime
import time
from utils.logger_utils import setup_logging
import requests
from utils.file_utils import create_output_dir, write_response_to_csv
from utils.api_utils import get_response


#Load the environment variables
load_dotenv()

logger = setup_logging()

timestamps = {
    "start_time": None,
    "download_end_time": None,
    "write_end_time": None
    
}

def get_csv(url: str, csv_output_name: str, folder_path: str) -> None:

    """
    Make a request to download a CSV file
    """

    logger.info(f"Downloading {csv_output_name} from {url}...")
    

    timestamps["start_time"] = datetime.datetime.now()
    logger.info(f"Download start time: {timestamps['start_time']}")

    try:
        create_output_dir(folder_path)
        response = get_response(url=url)
        if(response):
            timestamps["download_end_time"] = datetime.datetime.now()
            logger.info(f"Download end time: {timestamps["download_end_time"]}")
            
            file_path = f"{folder_path}/{csv_output_name}"

            write_response_to_csv(response, file_path)
            
            timestamps["write_end_time"] = datetime.datetime.now()
            logger.info(f"Download complete for {csv_output_name}, saved to {file_path}")
            logger.info(f"Time to download and process: {timestamps["write_end_time"] - timestamps["start_time"]}")

            
    except Exception as e:
        logger.error(f"Error getting response for {csv_output_name}: {e}")



def download_realtor_data(folder_path: str) -> None:
    
    """
    Download the Realtor.com CSV files
    
    Parameters:
    folder_path (str): The folder path to save the CSV files
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
        get_csv(url=url, csv_output_name=csv_output_name, folder_path=folder_path)

def main() -> None:

    folder_path = "/Users/jakegussler/Projects/RealtyInsights/data/raw/realtor"

    #Download the zillow tables
    download_realtor_data(folder_path)

if __name__ == "__main__":
    main()


    

