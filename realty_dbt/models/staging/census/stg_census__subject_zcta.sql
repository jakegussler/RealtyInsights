{{
  config(
    materialized='view',
  )
}}

{% set census_variables = {
    'median_household_income_estimate': 'NUMERIC(18,2)',
    'median_household_income_moe': 'NUMERIC(18,2)',
    'population_below_poverty_level_estimate': 'NUMERIC(18,2)',
    'population_below_poverty_level_moe': 'NUMERIC(18,2)',
    'population_below_poverty_level_under_18_estimate': 'INTEGER',
    'population_below_poverty_level_under_18_moe': 'INTEGER'
} %}

{% set extra_columns = [
    {"source": '"zip code tabulation area"', "alias": "zcta"}
] %}

select * from {{ build_census_view(source('census', 'census_acs5_subject_zcta'), extra_columns, census_variables) }}