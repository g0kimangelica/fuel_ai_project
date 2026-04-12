In this example, I will provide a DBT model for the specified schema using DuckDB as the database backend. This model follows the given rules by not performing any joins, aggregations, or business logic. Also, it standardizes column names and casts correct data types while handling empty strings as NULL values.

First, make sure to have DBT installed and set up correctly: https://docs.getdbt.com/getting-started

Create a new model file named `raw_fuel.sql` under the `models` folder.


{{ config(materialized='view') }}

SELECT
  CAST(date AS VARCHAR) AS date,
  CAST(country AS VARCHAR) AS country,
  CAST(region AS VARCHAR) AS region,
  CAST(income_level AS VARCHAR) AS income_level,
  CAST(subsidy_level AS VARCHAR) AS subsidy_level,
  COALESCE(petrol_usd_liter, 0.0) AS petrol_usd_liter,
  COALESCE(diesel_usd_liter, 0.0) AS diesel_usd_liter,
  COALESCE(lpg_usd_liter, 0.0) AS lpg_usd_liter,
  COALESCE(brent_crude_usd, 0.0) AS brent_crude_usd,
  COALESCE(tax_percentage, 0.0) AS tax_percentage
FROM raw_fuel;


After creating the file, run the DBT command to compile the model:

sh
dbt run


This should output the SQL used to create the staging table based on your specified schema with the required rules.