import os
import logging
from typing import Dict, Any
from download.download_realtor import download_realtor_data
from ingest.ingest_csv_to_db import ingest_realtor_data
from utils.file_utils import get_project_path
from utils.census_utils import load_census_config 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_pipeline_config() -> Dict[str, Any]:
    """
    Create unified configuration for the pipeline
    """
    project_path = get_project_path()
    config_path = os.path.join(project_path, 'config/census_variables.yml')
    
    return {
        'project_path': project_path,
        'folder_path': os.path.join(project_path, 'data/raw/realtor'),
    }

def run_download(folder_path: str, **kwargs) -> None:
    """Wrapper function for download process"""
    try:
        # Modify the main function to accept parameters
        download_realtor_data(folder_path)
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise

def run_ingest(folder_path: str, **kwargs) -> None:
    """Wrapper function for ingestion process"""
    try:
        # Call ingest_census_data directly instead of main
        ingest_realtor_data(folder_path)
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise

def run_pipeline(config: Dict[str, Any] = None) -> None:
    """
    Main pipeline function that orchestrates the entire process
    """
    if config is None:
        config = setup_pipeline_config()
    
    logger.info("Starting census data pipeline")
    
    try:
        # Run download
        logger.info("Starting download process")
        run_download(**config)
        
        # Run ingest
        logger.info("Starting ingest process")
        run_ingest(**config)
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    pipeline_config = setup_pipeline_config()
    run_pipeline(pipeline_config)