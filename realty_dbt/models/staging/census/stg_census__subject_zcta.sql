{% set census_variables = get_census_subject_variables() %}
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

with cleaned_data as (
    SELECT
        name::TEXT AS name,
        geo_id::TEXT AS geo_id,
        "zip code tabulation area"::TEXT AS zcta,
        year::INTEGER AS year,
        {% for col, col_type in census_variables.items() %}
            {{ clean_census_value(col, col_type) }} AS {{ col }}{% if not loop.last %},{% endif %}
        {% endfor %}
    FROM {{ source('census', 'census_acs5_subject_zcta') }}
)
select * from cleaned_data