{% macro get_census_subject_variables() %}
    {% set census_variables = {
        'median_household_income_estimate': 'NUMERIC(18,2)',
        'median_household_income_moe': 'NUMERIC(18,2)',
        'population_below_poverty_level_estimate': 'NUMERIC(18,2)',
        'population_below_poverty_level_moe': 'NUMERIC(18,2)',
        'population_below_poverty_level_under_18_estimate': 'INTEGER',
        'population_below_poverty_level_under_18_moe': 'INTEGER'
    } %}
    {{ return(census_variables) }}
{% endmacro %}