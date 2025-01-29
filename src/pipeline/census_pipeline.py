import os
import logging
from typing import Dict, Any
import download.download_census as download_census
import transform.transform_census as transform_census
import ingest.ingest_csv_to_db as ingest_csv_to_db
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
        'config_path': config_path,
        'raw_folder': os.path.join(project_path, 'data/raw/census'),
        'processed_folder': os.path.join(project_path, 'data/processed/census'),
        'census_config': load_census_config(config_path)
    }

def run_download(project_path: str, config_path: str, census_config: Dict[str, Any], **kwargs) -> None:
    """Wrapper function for download process"""
    try:
        # Modify the main function to accept parameters
        download_census.main(
            project_path=project_path,
            config_path=config_path,
            config=census_config
        )
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise

def run_transform(project_path: str, raw_folder: str, config_path: str, census_config: Dict[str, Any], **kwargs) -> None:
    """Wrapper function for transform process"""
    try:
        transform_census.main(
            project_path=project_path,
            census_raw_folder=raw_folder,
            config_path=config_path,
            config=census_config
        )
    except Exception as e:
        logger.error(f"Transform failed: {str(e)}")
        raise

def run_ingest(project_path: str, processed_folder: str, **kwargs) -> None:
    """Wrapper function for ingestion process"""
    try:
        # Call ingest_census_data directly instead of main
        ingest_csv_to_db.ingest_census_data()
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
        
        # Run transform
        logger.info("Starting transform process")
        run_transform(**config)
        
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