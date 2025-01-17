import yaml
from typing import Dict, List, Optional
import os

SUFFIXES = {
    'M': 'margin_of_error',
    'EA': 'annotation',
    'MA': 'margin_annotation',
    'PE': 'percentage',
}

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

    # Dynamically create census code based on variable configuration
    variable_code = table
    if column is not None:
        variable_code += f"_{column}"
    if row is not None:
        variable_code += f"_{row}"
    
    return f"{variable_code}{suffix}"

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
        table_prefix = variable_config.get('table', '')[0]
        for suffix in config['suffixes'].get(table_prefix, {}):
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

def get_readable_column_name(var_name: str, suffix: dict, suffix_mappings: dict) -> str:
    """Get a human-readable column name for a variable and suffix."""
    if suffix['code'] == 'E':  # Base estimate
        return var_name
    
    mapping = suffix_mappings.get(suffix['code'], suffix['code'].lower())
    return f"{var_name}_{mapping}"

def create_column_mapping(config: dict) -> Dict[str, str]:
    """
    Create a mapping from Census codes to human-readable names.
    Uses variable names as base for column names with suffixes for different measures.
    """
    mapping = {}
    
    # Add default columns to mapping
    for col in config['default_columns']:
        mapping[col['name']] = col['name'].lower()

    
    for var_name, var_config in config['variables'].items():
        # Get table prefix for variable
        table_prefix = var_config.get('table', '')[0]

        # Map year-specific variables
        if var_config.get('years') is not None:
            # Loop through year-specific configurations
            for year, year_config in var_config['years'].items():
                # Generate variable code for each suffix based on table prefix
                for suffix in config['suffixes'].get(table_prefix, {}):
                    variable_code = generate_variable_code(var_config, suffix['code'], year)
                    readable_name = get_readable_column_name(var_name, suffix, year)

                    mapping[variable_code] = readable_name.lower()
        # Map standard variables
        for suffix in config['suffixes'].get(table_prefix, {}):
            variable_code = generate_variable_code(var_config, suffix['code'])
            readable_name = get_readable_column_name(var_name, suffix)
            
            mapping[variable_code] = readable_name.lower()
    
    return mapping