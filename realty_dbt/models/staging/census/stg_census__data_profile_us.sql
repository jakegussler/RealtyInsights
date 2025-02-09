{{ config(
    materialized='view'
) }}

{% set census_variables = {
    'housing_units_total_estimate': 'INTEGER',
    'housing_units_total_moe': 'INTEGER',
    'housing_units_occupied_estimate': 'INTEGER',
    'housing_units_occupied_moe': 'INTEGER',
    'housing_units_vacant_estimate': 'INTEGER',
    'housing_units_vacant_moe': 'INTEGER',
    'housing_homeowner_vacancy_rate_estimate': 'NUMERIC(18,2)',
    'housing_homeowner_vacancy_rate_moe': 'NUMERIC(18,2)',
    'housing_rental_vacancy_rate_estimate': 'NUMERIC(18,2)',
    'housing_rental_vacancy_rate_moe': 'NUMERIC(18,2)',
    'housing_total_units_1_detached_estimate': 'INTEGER',
    'housing_total_units_1_detached_moe': 'INTEGER',
    'housing_total_units_1_attached_estimate': 'INTEGER',
    'housing_total_units_1_attached_moe': 'INTEGER',
    'housing_total_units_2_estimate': 'INTEGER',
    'housing_total_units_2_moe': 'INTEGER',
    'housing_total_units_3_to_4_estimate': 'INTEGER',
    'housing_total_units_3_to_4_moe': 'INTEGER',
    'housing_total_units_5_to_9_estimate': 'INTEGER',
    'housing_total_units_5_to_9_moe': 'INTEGER',
    'housing_total_units_10_to_19_estimate': 'INTEGER',
    'housing_total_units_10_to_19_moe': 'INTEGER',
    'housing_total_units_20_or_more_estimate': 'INTEGER',
    'housing_total_units_20_or_more_moe': 'INTEGER',
    'housing_total_units_mobile_home_estimate': 'INTEGER',
    'housing_total_units_mobile_home_moe': 'INTEGER',
    'housing_total_units_boat_rv_van_etc_estimate': 'INTEGER',
    'housing_total_units_boat_rv_van_etc_moe': 'INTEGER',
    'housing_built_2020_or_later_estimate': 'INTEGER',
    'housing_built_2020_or_later_moe': 'INTEGER',
    'housing_built_2010_to_2019_estimate': 'INTEGER',
    'housing_built_2010_to_2019_moe': 'INTEGER',
    'housing_built_2000_to_2009_estimate': 'INTEGER',
    'housing_built_2000_to_2009_moe': 'INTEGER',
    'housing_built_1990_to_1999_estimate': 'INTEGER',
    'housing_built_1990_to_1999_moe': 'INTEGER',
    'housing_built_1980_to_1989_estimate': 'INTEGER',
    'housing_built_1980_to_1989_moe': 'INTEGER',
    'housing_built_1970_to_1979_estimate': 'INTEGER',
    'housing_built_1970_to_1979_moe': 'INTEGER',
    'housing_built_1960_to_1969_estimate': 'INTEGER',
    'housing_built_1960_to_1969_moe': 'INTEGER',
    'housing_built_1950_to_1959_estimate': 'INTEGER',
    'housing_built_1950_to_1959_moe': 'INTEGER',
    'housing_built_1940_to_1949_estimate': 'INTEGER',
    'housing_built_1940_to_1949_moe': 'INTEGER',
    'housing_built_1939_or_earlier_estimate': 'INTEGER',
    'housing_built_1939_or_earlier_moe': 'INTEGER',
    'housing_bedrooms_0_estimate': 'INTEGER',
    'housing_bedrooms_0_moe': 'INTEGER',
    'housing_bedrooms_1_estimate': 'INTEGER',
    'housing_bedrooms_1_moe': 'INTEGER',
    'housing_bedrooms_2_estimate': 'INTEGER',
    'housing_bedrooms_2_moe': 'INTEGER',
    'housing_bedrooms_3_estimate': 'INTEGER',
    'housing_bedrooms_3_moe': 'INTEGER',
    'housing_bedrooms_4_estimate': 'INTEGER',
    'housing_bedrooms_4_moe': 'INTEGER',
    'housing_bedrooms_5_or_more_estimate': 'INTEGER',
    'housing_bedrooms_5_or_more_moe': 'INTEGER',
    'housing_owner_occupided_value_under_50_estimate': 'INTEGER',
    'housing_owner_occupided_value_under_50_moe': 'INTEGER',
    'housing_owner_occupided_value_50_to_99_estimate': 'INTEGER',
    'housing_owner_occupided_value_50_to_99_moe': 'INTEGER',
    'housing_owner_occupided_value_100_to_149_estimate': 'INTEGER',
    'housing_owner_occupided_value_100_to_149_moe': 'INTEGER',
    'housing_owner_occupided_value_150_to_199_estimate': 'INTEGER',
    'housing_owner_occupided_value_150_to_199_moe': 'INTEGER',
    'housing_owner_occupided_value_200_to_299_estimate': 'INTEGER',
    'housing_owner_occupided_value_200_to_299_moe': 'INTEGER',
    'housing_owner_occupided_value_300_to_499_estimate': 'INTEGER',
    'housing_owner_occupided_value_300_to_499_moe': 'INTEGER',
    'housing_owner_occupided_value_500_to_999_estimate': 'INTEGER',
    'housing_owner_occupided_value_500_to_999_moe': 'INTEGER',
    'housing_owner_occupided_value_1000_or_more_estimate': 'INTEGER',
    'housing_owner_occupided_value_1000_or_more_moe': 'INTEGER',
    'housing_units_with_mortgage_estimate': 'INTEGER',
    'housing_units_with_mortgage_moe': 'INTEGER',
    'housing_units_without_mortgage_estimate': 'INTEGER',
    'housing_units_without_mortgage_moe': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_20_pct_or_less_estimate': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_20_pct_or_less_moe': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_20_to_24_9_pct_estimate': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_20_to_24_9_pct_moe': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_25_to_29_9_pct_estimate': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_25_to_29_9_pct_moe': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_30_to_34_9_pct_estimate': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_30_to_34_9_pct_moe': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_35_pct_or_more_estimate': 'INTEGER',
    'housing_smocapi_total_mortgaged_houses_35_pct_or_more_moe': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_10_pct_or_less_estimate': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_10_pct_or_less_moe': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_15_to_19_9_pct_estimate': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_15_to_19_9_pct_moe': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_20_to_24_9_pct_estimate': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_20_to_24_9_pct_moe': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_25_to_29_9_pct_estimate': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_25_to_29_9_pct_moe': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_30_to_34_9_pct_estimate': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_30_to_34_9_pct_moe': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_35_pct_or_more_estimate': 'INTEGER',
    'housing_smocapi_total_non_mortgaged_houses_35_pct_or_more_moe': 'INTEGER',
    'housing_rent_gross_reported_500_or_under_estimate': 'INTEGER',
    'housing_rent_gross_reported_500_or_under_moe': 'INTEGER',
    'housing_rent_gross_reported_500_to_999_estimate': 'INTEGER',
    'housing_rent_gross_reported_500_to_999_moe': 'INTEGER',
    'housing_rent_gross_reported_1000_to_1499_estimate': 'INTEGER',
    'housing_rent_gross_reported_1000_to_1499_moe': 'INTEGER',
    'housing_rent_gross_reported_1500_to_1999_estimate': 'INTEGER',
    'housing_rent_gross_reported_1500_to_1999_moe': 'INTEGER',
    'housing_rent_gross_reported_2000_to_2499_estimate': 'INTEGER',
    'housing_rent_gross_reported_2000_to_2499_moe': 'INTEGER',
    'housing_rent_gross_reported_2500_to_2999_estimate': 'INTEGER',
    'housing_rent_gross_reported_2500_to_2999_moe': 'INTEGER',
    'housing_rent_gross_reported_3000_or_more_estimate': 'INTEGER',
    'housing_rent_gross_reported_3000_or_more_moe': 'INTEGER',
    'housing_rent_gross_reported_median_dollars_estimate': 'INTEGER',
    'housing_rent_gross_reported_median_dollars_moe': 'INTEGER',
    'housing_rent_gross_reported_no_rent_paid_estimate': 'INTEGER',
    'housing_rent_gross_reported_no_rent_paid_moe': 'INTEGER',
    'housing_rent_grapi_15_pct_or_less_estimate': 'INTEGER',
    'housing_rent_grapi_15_pct_or_less_moe': 'INTEGER',
    'housing_rent_grapi_15_to_19_9_pct_estimate': 'INTEGER',
    'housing_rent_grapi_15_to_19_9_pct_moe': 'INTEGER',
    'housing_rent_grapi_20_to_24_9_pct_estimate': 'INTEGER',
    'housing_rent_grapi_20_to_24_9_pct_moe': 'INTEGER',
    'housing_rent_grapi_25_to_29_9_pct_estimate': 'INTEGER',
    'housing_rent_grapi_25_to_29_9_pct_moe': 'INTEGER',
    'housing_rent_grapi_30_to_34_9_pct_estimate': 'INTEGER',
    'housing_rent_grapi_30_to_34_9_pct_moe': 'INTEGER',
    'housing_rent_grapi_35_pct_or_more_estimate': 'INTEGER',
    'housing_rent_grapi_35_pct_or_more_moe': 'INTEGER',
    'population_total_estimate': 'INTEGER',
    'population_total_moe': 'INTEGER',
    'population_male_estimate': 'INTEGER',
    'population_male_moe': 'INTEGER',
    'population_female_estimate': 'INTEGER',
    'population_female_moe': 'INTEGER',
    'population_age_under_5_estimate': 'INTEGER',
    'population_age_under_5_moe': 'INTEGER',
    'population_age_5_to_9_estimate': 'INTEGER',
    'population_age_5_to_9_moe': 'INTEGER',
    'population_age_10_to_14_estimate': 'INTEGER',
    'population_age_10_to_14_moe': 'INTEGER',
    'population_age_15_to_19_estimate': 'INTEGER',
    'population_age_15_to_19_moe': 'INTEGER',
    'population_age_20_to_24_estimate': 'INTEGER',
    'population_age_20_to_24_moe': 'INTEGER',
    'population_age_25_to_34_estimate': 'INTEGER',
    'population_age_25_to_34_moe': 'INTEGER',
    'population_age_35_to_44_estimate': 'INTEGER',
    'population_age_35_to_44_moe': 'INTEGER',
    'population_age_45_to_54_estimate': 'INTEGER',
    'population_age_45_to_54_moe': 'INTEGER',
    'population_age_55_to_59_estimate': 'INTEGER',
    'population_age_55_to_59_moe': 'INTEGER',
    'population_age_60_to_64_estimate': 'INTEGER',
    'population_age_60_to_64_moe': 'INTEGER',
    'population_age_65_to_74_estimate': 'INTEGER',
    'population_age_65_to_74_moe': 'INTEGER',
    'population_age_75_to_84_estimate': 'INTEGER',
    'population_age_75_to_84_moe': 'INTEGER',
    'population_age_85_and_over_estimate': 'INTEGER',
    'population_age_85_and_over_moe': 'INTEGER',
    'population_median_age_estimate': 'INTEGER',
    'population_median_age_moe': 'INTEGER',
    'population_race_white_estimate': 'INTEGER',
    'population_race_white_moe': 'INTEGER',
    'population_race_black_or_african_american_estimate': 'INTEGER',
    'population_race_black_or_african_american_moe': 'INTEGER',
    'population_race_american_indian_and_alaska_native_estimate': 'INTEGER',
    'population_race_american_indian_and_alaska_native_moe': 'INTEGER',
    'population_race_asian_estimate': 'INTEGER',
    'population_race_asian_moe': 'INTEGER',
    'population_race_native_hawaiian_and_other_pacific_islander_estimate': 'INTEGER',
    'population_race_native_hawaiian_and_other_pacific_islander_moe': 'INTEGER',
    'population_race_some_other_estimate': 'INTEGER',
    'population_race_some_other_moe': 'INTEGER',
    'population_latino_estimate': 'INTEGER',
    'population_latino_moe': 'INTEGER',
    'population_latino_mexican_estimate': 'INTEGER',
    'population_latino_mexican_moe': 'INTEGER',
    'population_latino_puerto_rican_estimate': 'INTEGER',
    'population_latino_puerto_rican_moe': 'INTEGER',
    'population_latino_cuban_estimate': 'INTEGER',
    'population_latino_cuban_moe': 'INTEGER',
    'population_latino_other_estimate': 'INTEGER',
    'population_latino_other_moe': 'INTEGER'
} %}

{% set extra_columns = [
    {"source": '"us"', "alias": "us"}
] %}

{{ build_census_staging(source('census', 'census_acs5_data_profile_us'), extra_columns, census_variables) }}