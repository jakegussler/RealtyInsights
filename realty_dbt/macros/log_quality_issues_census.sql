{% macro log_quality_issues_census(source_table, columns) %}

insert into {{ ref('stg_census__data_quality_issues') }} (
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
from {{ source_table }} src
cross join lateral (
    values
    {% for column in columns %}
        ('{{ column }}', src.{{ column }}){% if not loop.last %},{% endif %}
{% endfor %}
) as col(column_name, value)
inner join {{ ref('census__value_annotations') }} va
    on col.value = va.value_code
where col.value in (
    select value_code from {{ ref('census__value_annotations') }}
    where value_code is not null
)
or col.value is null

{% endmacro %}
