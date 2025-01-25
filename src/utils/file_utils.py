import os
from utils.logger_utils import setup_logging
from pathlib import Path

logger = setup_logging()


def create_output_dir(folderpath: str) -> None:
    try:
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
            logger.info(f"Created directory: {folderpath}")
    except OSError as e:
        logger.error(f"Error creating directory {folderpath}: {e}")
        raise

def write_response_to_csv(response, file_path: str) -> None:
    try:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.info(f"Saved response to {file_path}")
    except (IOError, OSError) as e:
        logger.error(f"Failed to write response to {file_path}: {e}")
        raise

def write_df_to_csv(df, file_path: str, append: bool = False) -> None:
    try:
        if append:
            # Append to the file, avoid writing the header if the file exists
            df.to_csv(file_path, index=False, mode='a', header=not os.path.exists(file_path))
        else:
            # Overwrite the file
            df.to_csv(file_path, index=False)
        logger.info(f"Saved data to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data to {file_path}: {e}")
        raise IOError(f"Failed to write DataFrame to CSV: {e}") from e

def delete_csv(file_path: str) -> None:
    logger.info(f"Checking if CSV fie exists at {file_path}")
    if os.path.exists(file_path):
        logger.info(f"CSV file exists, deleting {file_path}")
        try:
            os.remove(file_path)
            logger.info(f"Deleted {file_path}")
        except Exception as e:
            logger.error(f"Error deleting {file_path}: {e}")
    else:
        logger.info(f"CSV file does not exist at {file_path}, ignoring delete request")

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
        raise

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
        raise

def get_project_path() -> str:
    try:
        Path(__file__).parent.parent.resolve()
    except Exception as e:
        logger.error(f"Error getting project path: {e}")
        raise

