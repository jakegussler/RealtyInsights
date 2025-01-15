import os
from utils.logger_utils import setup_logging

logger = setup_logging()


def create_output_dir(folderpath: str) -> None:

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        logger.info(f"Created directory: {folderpath}")

def write_response_to_csv(response, filepath: str) -> None:

    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def write_df_to_csv(df, filepath: str, append: bool = False) -> None:
    try:
        if append:
            # Append to the file, avoid writing the header if the file exists
            df.to_csv(filepath, index=False, mode='a', header=not os.path.exists(filepath))
        else:
            # Overwrite the file
            df.to_csv(filepath, index=False)
        logger.info(f"Saved data to {filepath}")
    except Exception as e:
        logger.error(f"Error saving data to {filepath}: {e}")

def delete_csv(filepath: str) -> None:
    logger.info(f"Checking if CSV fie exists at {filepath}")
    if os.path.exists(filepath):
        logger.info(f"CSV file exists, deleting {filepath}")
        try:
            os.remove(filepath)
            logger.info(f"Deleted {filepath}")
        except Exception as e:
            logger.error(f"Error deleting {filepath}: {e}")
    else:
        logger.info(f"CSV file does not exist at {filepath}, ignoring delete request")

def clean_folder(folder_path: str) -> None:
    """
    Clean the folder by deleting any existing files
    Parameters:
    folder_path (str): The path to the folder to clean
    """
    try:
        logger.info(f"Cleaning folder {folder_path}")
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                logger.info(f"Deleting existing CSV file: {file}")
                delete_csv(os.path.join(folder_path, file))
    except Exception as e:
        logger.error(f"Error cleaning folder {folder_path}: {e}")

def prepare_and_clean_folder(folder_path: str) -> None:
    """
    Prepare a folder by creating output directory
    then deleting any existing files if output directory exists
    Parameters:
    folder_path (str): The path to the folder to prepare
    """
    try:
        logger.info(f"Preparing folder {folder_path}")
        logger.info(f"Creating output directory if it does not exist")
        create_output_dir(folder_path)
        clean_folder(folder_path)
    except Exception as e:
        logger.error(f"Error preparing folder {folder_path}: {e}")

