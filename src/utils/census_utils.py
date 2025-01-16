import yaml
from typing import Dict, List, Optional
import os

def load_census_config(config_path: str) -> dict:
    """Load the census configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def generate_variable_code(
    variable_config: dict,
    year: int,
    suffix: str
) -> str:
    """Generate a Census variable code for a specific year and suffix."""
    # Get year-specific configuration if it exists
    year_config = variable_config.get('years', {}).get(year, {})
    
    # Use year-specific values or defaults
    column = year_config.get('column', variable_config['column'])
    row = year_config.get('row', variable_config['row'])
    table = year_config.get('table', variable_config['table'])
    
    return f"{table}_{column}_{row}{suffix}"

def get_all_variable_codes(
    config: dict,
    year: int
) -> List[str]:
    """Generate all variable codes for a given year."""
    codes = []
    
    # Add default columns first
    codes.extend(col['name'] for col in config['default_columns'])
    
    # Generate codes for each variable with all suffixes
    for variable_name, variable_config in config['variables'].items():
        for suffix in config['suffixes']:
            code = generate_variable_code(
                variable_config,
                year,
                suffix['code']
            )
            codes.append(code)
    
    return codes

def get_column_string(config: dict, year: int) -> str:
    """Get the complete column string for the API request."""
    return ','.join(get_all_variable_codes(config, year))

def create_column_mapping(config: dict) -> Dict[str, str]:
    """
    Create a mapping from Census codes to human-readable names.
    Uses variable names as base for column names with suffixes for different measures.
    """
    mapping = {}
    
    # Add default columns to mapping
    for col in config['default_columns']:
        mapping[col['name']] = col['name'].lower()
    
    # Add mappings for each variable and suffix combination
    for var_name, var_config in config['variables'].items():
        for suffix in config['suffixes']:
            census_code = f"{var_config['table']}_{var_config['column']}_{var_config['row']}{suffix['code']}"
            
            # Create snake_case column name from variable name and suffix
            if suffix['code'] == 'E':  # Base estimate
                readable_name = var_name
            else:
                suffix_type = {
                    'M': 'margin_of_error',
                    'EA': 'annotation',
                    'MA': 'margin_annotation'
                }.get(suffix['code'], suffix['code'].lower())
                readable_name = f"{var_name}_{suffix_type}"
            
            mapping[census_code] = readable_name.lower()
    
    return mapping