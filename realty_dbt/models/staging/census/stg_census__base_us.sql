{{ config(
    materialized='view'
) }}



{% set census_variables = {
    'median_rent_estimate': 'NUMERIC(18,2)',
    'median_rent_moe': 'NUMERIC(18,2)',
    'median_rent_studio_estimate': 'NUMERIC(18,2)',
    'median_rent_studio_moe': 'NUMERIC(18,2)',
    'median_rent_1_bedroom_estimate': 'NUMERIC(18,2)',
    'median_rent_1_bedroom_moe': 'NUMERIC(18,2)',
    'median_rent_2_bedroom_estimate': 'NUMERIC(18,2)',
    'median_rent_2_bedroom_moe': 'NUMERIC(18,2)',
    'median_rent_3_bedroom_estimate': 'NUMERIC(18,2)',
    'median_rent_3_bedroom_moe': 'NUMERIC(18,2)',
    'median_rent_4_bedroom_estimate': 'NUMERIC(18,2)',
    'median_rent_4_bedroom_moe': 'NUMERIC(18,2)',
    'median_rent_5_bedroom_estimate': 'NUMERIC(18,2)',
    'median_rent_5_bedroom_moe': 'NUMERIC(18,2)',
    'residences_total_estimate': 'INTEGER',
    'residences_total_moe': 'INTEGER',
    'residences_studio_estimate': 'INTEGER',
    'residences_studio_moe': 'INTEGER',
    'residences_1_bedroom_estimate': 'INTEGER',
    'residences_1_bedroom_moe': 'INTEGER',
    'residences_2_bedroom_estimate': 'INTEGER',
    'residences_2_bedroom_moe': 'INTEGER',
    'residences_3_bedroom_estimate': 'INTEGER',
    'residences_3_bedroom_moe': 'INTEGER',
    'residences_4_bedroom_estimate': 'INTEGER',
    'residences_4_bedroom_moe': 'INTEGER',
    'residences_5_bedroom_estimate': 'INTEGER',
    'residences_5_bedroom_moe': 'INTEGER'
} %}

{% set extra_columns = [
    {"source": "us", "alias": "us"}
] %}

{{ build_census_staging(source('census', 'census_acs5_base_us'), extra_columns, census_variables) }}