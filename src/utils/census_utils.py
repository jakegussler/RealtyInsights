import yaml
from typing import Dict, List, Optional
import os
from utils.logger_utils import setup_logging

logger = setup_logging()

def get_table_names(config: dict) -> List[str]:
    """Get all table names from configuration."""
    return config['table_types'].values()


def load_census_config(config_path: str) -> dict:
    """Load the census configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def generate_variable_code(
    variable_config: dict,
    suffix: str,
    year: int=None
) -> str | None:
    """Generate a Census variable code for a specific year and suffix."""
    # Get year-specific configuration if it exists
    try:
        year_config = variable_config.get('overrides', {}).get(year, {})
        if year_config.get('missing', {}) is True:
            return None
    except AttributeError:
        logger.error(f"Error getting year-specific configuration for {variable_config}")
        raise
    
    # Use year-specific values or defaults
    try:
        table = year_config.get('table', variable_config.get('table'))
        column = year_config.get('column', variable_config.get('column'))
        row = year_config.get('row', variable_config.get('row'))
    except KeyError:
        logger.error(f"Error getting variable configuration for {variable_config}")
        raise
    
    # Dynamically create census code based on variable configuration
    try:
        variable_code = table
        if column is not None:
            variable_code += f"_{column}"
        if row is not None:
            variable_code += f"_{row}"
    except KeyError:
        logger.error(f"Error generating variable code for {variable_config}")
        raise

    return f"{variable_code}{suffix}"

def get_all_variable_codes(
    config: dict,
    year: int,
    table_name: str,
    variables: List[str]
) -> List[str]:
    """Generate all variable codes for a given year."""
    codes = []
    
    # Add default columns first
    codes.extend(col['name'] for col in config['default_columns'])

    # Generate codes for each variable with all suffixes
    for variable in variables:
        variable_config = config['variables'][table_name][variable]
        for suffix in config['suffixes']:
            code = generate_variable_code(
                variable_config,
                suffix['code'],
                year
            )
            if code is not None:
                codes.append(code)
    
    return codes

def get_column_string(
        config: dict,
        year: int, 
        table_name: str, 
        variables: List[str]
    ) -> str:
    """Get the complete column string for the API request."""
    return ','.join(get_all_variable_codes(config, year, table_name, variables))


def create_column_mapping(config: dict) -> Dict[str, str]:
    """
    Create a mapping from Census codes to human-readable names.
    Uses variable names as base for column names with suffixes for different measures.
    """
    mapping = {}
    
    # Add default columns to mapping
    for col in config['default_columns']:
        mapping[col['name']] = col['name'].lower()

    
    for table_name, table_config in config['variables'].items():

        for var_name, var_config in table_config.items():
            # Map year-specific variables
            if var_config.get('overrides') is not None:
                # Loop through year-specific configurations
                for year, year_config in var_config['overrides'].items():
                    # Generate variable code for each suffix based on table prefix
                    for suffix in config['suffixes']:
                        variable_code = generate_variable_code(var_config, suffix['code'], year)
                        readable_name = f"{var_name}_{suffix['mapping'].lower()}"

                        mapping[variable_code] = readable_name.lower()
                # Map standard variables
                for suffix in config['suffixes']:
                    variable_code = generate_variable_code(var_config, suffix['code'])
                    readable_name = f"{var_name}_{suffix['mapping'].lower()}"
                    
                    mapping[variable_code] = readable_name.lower()
    
    return mapping