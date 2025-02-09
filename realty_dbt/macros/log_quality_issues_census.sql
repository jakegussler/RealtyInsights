{% macro log_quality_issues_census(source_table, columns) %}

insert into {{ ref('stg_census__data_quality_issues') }} (
    source,
    source_table,
    key_columns,
    column_name,
    issue_type,
    issue_description,
    original_value,
    cleaned_value,
    detection_timestamp,
    notes
)
select 
    {{ dbt_utils.generate_surrogate_key(['source', 'source_table', 'column_name', 'detection_timestamp']) }} as issue_id,
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
    null as cleaned_value,
    current_timestamp as detection_timestamp,
    null as notes

from {{ source_table }} src
cross join lateral (
    values
    {% for column in columns %}
        ('{{ column }}', src.{{ column }}){% if not loop.last %},{% endif %}
{% endfor %}
) as col(column_name, value)
inner join {{ ref('census__value_annotations') }} va
    on col.value::text = va.value_code::text
where col.value::text in (
    select value_code::text from {{ ref('census__value_annotations') }}
    where value_code::text is not null
)
or col.value is null

{% endmacro %}
