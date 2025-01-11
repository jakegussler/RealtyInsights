import os
from utils.logger_utils import setup_logging

logger = setup_logging()


def create_output_dir(folderpath):

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        logger.info(f"Created directory: {folderpath}")

def write_response_to_csv(response, filepath):

    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)