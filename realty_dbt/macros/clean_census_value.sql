{% macro clean_census_value(col, col_type) %}
    case when {{ col }} in (select value_code from {{ ref('census__value_annotations') }} where value_code is not null) 
         then null 
         else  cast({{ col }} as {{ col_type }})
    end
{% endmacro %}
