import pandas as pd
import os
from pathlib import Path
from utils.logger_utils import setup_logging
from utils.file_utils import write_df_to_csv, prepare_and_clean_folder, get_project_path
from utils.census_utils import load_census_config, create_column_mapping

logger = setup_logging()

def add_year_column(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Add year column to DataFrame."""
    try:
        logger.info("Adding year column to DataFrame")
        df['year'] = year
        return df
    except Exception as e:
        logger.error(f"Error adding year column for {year}: {e}")
        return df

def get_year_from_file_name(file_name: str) -> str:
    """Extract year from filename."""
    try:
        return file_name.split('.')[0].split('_')[-2]
    except Exception as e:
        logger.error(f"Error getting year from filename {file_name}: {e}")
        return None
    
def get_base_name(file_name):
   """Get base table name by removing suffix after second-to-last underscore."""
   return file_name.rsplit('_', 2)[0]

def get_consolidated_file_name(file_name: str) -> str:
    """Get consolidated file name based"""
    return f"{get_base_name(file_name)}.csv"

def get_processed_file_path(raw_file_path: str) -> str:
    file_name = os.path.basename(raw_file_path)
    return os.path.join(
        get_project_path(),
        "data/processed/census",
        get_consolidated_file_name(file_name)
    )

def map_columns(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """Map DataFrame columns using configuration."""
    try:
        # Get the intersection of DataFrame columns and mapping keys
        columns_to_map = {
            col: column_mapping[col] 
            for col in df.columns 
            if col in column_mapping
        }
        logger.debug(f"Mapping columns: {columns_to_map}")
        return df.rename(columns=columns_to_map)
    except Exception as e:
        logger.error(f"Error mapping columns: {e}")
        return df

def remove_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Remove specified column from DataFrame."""
    try:
        if column in df.columns:
            logger.info(f"Removing column: {column}")
            return df.drop(columns=[column])
        logger.info(f"Column {column} not found in DataFrame")
        return df
    except Exception as e:
        logger.error(f"Error removing column {column}: {e}")
        return df
    
def merge_files_with_same_base(raw_file_path):
    base_file_name = Path(raw_file_path).stem.split('_0')[0]

    logger.info(f"Checking for matching files with base name: {base_file_name}")
    directory = os.path.dirname(raw_file_path)
    matching_files = [f for f in os.listdir(directory) if base_file_name in f]
    logger.info(f"Found {len(matching_files)} matching files")

    if len(matching_files) == 1:
        logger.info(f"Only one file found. Returning DataFrame")
        return pd.read_csv(raw_file_path)
        
    dfs = []
    for file in matching_files:
        file_path = os.path.join(directory, file)
        logger.info(f"Reading file: {file_path}")
        # Check if columns already exist in merged DataFrame to avoid duplicates
        df = pd.read_csv(file_path, low_memory=False)
        if len(dfs) > 0:
            existing_cols = set().union(*[set(df.columns) for df in dfs])
            cols_to_keep = ['GEO_ID'] + [col for col in df.columns if col not in existing_cols]
            df = df[cols_to_keep]

        dfs.append(df)

    # Merge all dataframes with outer join on GEO_ID
    final_df = dfs[0]
    logger.info(f"Merging {len(dfs)} DataFrames")
    try:
        for df in dfs[1:]:
            final_df = pd.merge(final_df, df, on='GEO_ID', how='outer') 
    except Exception as e:
        logger.error(f"Error merging DataFrames: {e}")
        raise

    return final_df

def process_census_file(
    raw_file_path: str,
    processed_file_path: str,
    column_mapping: dict
) -> None:
    """Process a single census file."""
    logger.info(f"Processing file: {raw_file_path}")
    try:
        # Read and transform the file
        df = merge_files_with_same_base(raw_file_path)
        df = map_columns(df, column_mapping)
        df = add_year_column(df, int(get_year_from_file_name(raw_file_path)))
        df = remove_column(df, 'state')

        # Save the processed data
        write_df_to_csv(df, processed_file_path, append=True)
    except Exception as e:
        logger.error(f"Error processing file {raw_file_path}: {e}")

def process_and_consolidate_census_files(
    raw_folder_path: str,
    column_mapping: dict
) -> None:
    """Process all census files and consolidate into files based on table."""

    logger.info(f"Processing all files in {raw_folder_path}")

    # Create processed folder if it doesn't exist and delete existing files
    prepare_and_clean_folder(raw_folder_path.replace('raw', 'processed'))

    # Process each file in each census table folder
    for folder in os.listdir(raw_folder_path):
        # Create processed file path using table name from raw folder path being processed
        raw_subfolder_path = os.path.join(raw_folder_path, folder)

        # Process each file in the folder
        for file_name in os.listdir(os.path.join(raw_folder_path, folder)):
            # Process the first file for each year
            if file_name.endswith("_0.csv"):
                raw_file_path = os.path.join(raw_subfolder_path, file_name)
                processed_file_path = get_processed_file_path(raw_file_path)

                process_census_file(
                    raw_file_path=os.path.join(raw_subfolder_path, file_name),
                    processed_file_path=processed_file_path,
                    column_mapping=column_mapping
                )

def main() -> None:
    # Load paths from environment
    project_path = get_project_path()
    census_raw_folder = os.path.join(project_path, 'data/raw/census')

    config_path = os.path.join(project_path, 'config/census_variables.yml')

    # Load configuration and create column mapping
    config = load_census_config(config_path)
    column_mapping = create_column_mapping(config)

    # Process files
    logger.info(f"Processing census files in {census_raw_folder}")
    process_and_consolidate_census_files(
        raw_folder_path=census_raw_folder,
        column_mapping=column_mapping
    )
    print("Census data processing complete.")
if __name__ == "__main__":
    main()