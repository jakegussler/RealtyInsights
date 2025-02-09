{{ config(
    materialized='view',
    schema='logging'
) }}

with census_quality_issues as (
    select
        'census_data' as source,
        '{{ this.identifier }}' as source_table,
        jsonb_build_object(
            'zcta', src."zip code tabulation area",
            'year', src.year
        ) as key_columns,
        col.column_name,
        va.issue_type,
        va.issue_description as issue_description,
        col.value::text as original_value,
        null as cleaned_value,
        current_timestamp as detection_timestamp,
        null as notes
    from {{ source('census', 'census_acs5_subject_zcta') }} src
    cross join lateral (
        values 
            ('median_household_income_estimate', src.median_household_income_estimate),
            ('median_household_income_moe', src.median_household_income_moe),
            ('population_below_poverty_level_estimate', src.population_below_poverty_level_estimate),
            ('population_below_poverty_level_moe', src.population_below_poverty_level_moe),
            ('population_below_poverty_level_under_18_estimate', src.population_below_poverty_level_under_18_estimate),
            ('population_below_poverty_level_under_18_moe', src.population_below_poverty_level_under_18_moe)
    ) as col(column_name, value)
    inner join {{ ref('census__value_annotations') }} va
        on col.value::text = va.value_code::text
    where col.value::text in (
        select value_code::text 
        from {{ ref('census__value_annotations') }}
        where value_code::text is not null
    )
    or col.value is null
)

select 
    {{ dbt_utils.generate_surrogate_key(['source', 'source_table', 'column_name', 'detection_timestamp']) }} as issue_id,
    *
from census_quality_issues