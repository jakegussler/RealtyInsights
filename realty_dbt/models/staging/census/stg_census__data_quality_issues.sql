-- models/staging/census/stg_census__data_quality_issues.sql
{{ config(
    materialized='table',
    schema='stg_census'
) }}

WITH empty_dq_table AS (
    SELECT
        cast(null as bigint) as issue_id,
        cast(null as text) as source_system,
        cast(null as text) as source_table,
        cast(null as jsonb) as key_columns,
        cast(null as text) as column_name,
        cast(null as text) as issue_type,
        cast(null as text) as issue_description,
        cast(null as text) as original_value,
        cast(null as text) as cleaned_value,
        cast(null as timestamptz) as detection_timestamp,
        cast(null as text) as impact_description,
        cast(null as text) as notes
    WHERE false
)

SELECT 
    {{ dbt_utils.surrogate_key(['source_system', 'source_table', 'column_name', 'detection_timestamp']) }} as issue_id,
    *
FROM empty_dq_table