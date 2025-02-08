-- models/staging/stg_data_quality_issues.sql
{{ config(
    materialized='table',
    indexes=[
        {'columns': ['source_system', 'source_table']},
        {'columns': ['detection_timestamp']},
        {'columns': ['resolution_status']},
        {'columns': ['key_columns'], 'type': 'gin'}
    ]
) }}

CREATE TABLE IF NOT EXISTS {{ this }} (
    issue_id SERIAL PRIMARY KEY,
    source_system TEXT NOT NULL,
    source_table TEXT NOT NULL,
    key_columns JSONB NOT NULL,
    column_name TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    issue_description TEXT,
    original_value TEXT,
    cleaned_value TEXT,
    detection_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    impact_description TEXT,
    notes TEXT
)
