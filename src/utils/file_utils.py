import os
from utils.logger_utils import setup_logging

logger = setup_logging()

def create_folderpath_if_not_exists(folderpath):

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        logger.info(f"Created directory: {folderpath}")