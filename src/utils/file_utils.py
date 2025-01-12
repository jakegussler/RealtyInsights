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

def write_df_to_parquet(df, filepath: str) -> None:

    try:
        df.to_parquet(filepath)
        logger.info(f"Saved data to {filepath}")
    except Exception as e:
        logger.error(f"Error saving data to {filepath}: {e}")



