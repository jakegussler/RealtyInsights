{% macro build_census_staging(source, extra_columns, census_variables) %}
  with cleaned_data as (
    select
      -- Common columns
      name::TEXT as name,
      geo_id::TEXT as geo_id,
      {% for extra in extra_columns %}
        {{ extra.source }}::TEXT as {{ extra.alias }}{% if not loop.last or census_variables|length > 0 %}, {% endif %}
      {% endfor %}
      year::INTEGER as year
      {% if census_variables %}
        ,{% for col, col_type in census_variables.items() %}
          {{ clean_census_value(col, col_type) }} as {{ col }}{% if not loop.last %}, {% endif %}
        {% endfor %}
      {% endif %}
    from {{ source }}
  )
  select * from cleaned_data
{% endmacro %}