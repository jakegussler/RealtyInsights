-- macros/data_quality/log_quality_issues.sql
{% macro log_quality_issues_census(source_table, columns) %}

insert into {{ ref('stg_data_quality_issues') }} (
    source,
    source_table,
    key_columns,
    column_name,
    issue_type,
    issue_description,
    original_value,
    detection_method,
    severity
)
select 
    'census_data' as source,
    '{{ source_table }}' as source_table,
    jsonb_build_object(
        'zcta', src.zcta,
        'year', src.year
    ) as key_columns,
    col.column_name,
    va.issue_type,
    va.issue_description as issue_description,
    col.value::text as original_value,
    'dbt_transformation' as detection_method,
    case 
        when va.issue_type in ('insufficient_sample', 'insufficient_cases') then 'high'
        when va.issue_type in ('not_available', 'missing_data') then 'medium'
        else 'low'
    end as severity
from {{ source_table }} src
cross join lateral (
    values
    {% for column in columns %}
        ('{{ column }}', src.{{ column }}){% if not loop.last %},{% endif %}
    {% endfor %}
) as col(column_name, value)
inner join {{ ref('stg_value_annotations') }} va
    on col.value = va.value_code
    or (col.value is null and va.value_code is null)
where col.value in (
    select value_code from {{ ref('stg_value_annotations') }}
    where value_code is not null
)
or col.value is null

{% endmacro %}