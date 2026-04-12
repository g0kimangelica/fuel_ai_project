-- MART: fuel_prices_impact

WITH
pre_period AS (
    SELECT
        date,
        country,
        region,
        income_level,
        subsidy_level,
        AVG(petrol_usd_liter) AS pre_petrol,
        AVG(diesel_usd_liter) AS pre_diesel,
        AVG(lpg_usd_liter) AS pre_lpg
    FROM stg_fuel
    WHERE date < (SELECT start_date FROM events.event A LIMIT 1)
    GROUP BY country, region, income_level, subsidy_level
),

post_period AS (
    SELECT
        date,
        country,
        region,
        income_level,
        subsidy_level,
        AVG(petrol_usd_liter) AS post_petrol,
        AVG(diesel_usd_liter) AS post_diesel,
        AVG(lpg_usd_liter) AS post_lpg
    FROM stg_fuel
    WHERE date > (SELECT end_date FROM events.event A LIMIT 1)
    GROUP BY country, region, income_level, subsidy_level

-- Impact calculation and final selection
SELECT
    country,
    pre_petrol,
    post_petrol,
    post_petrol - pre_petrol AS impact,
    pre_diesel,
    post_diesel,
    post_diesel - pre_diesel AS diesel_impact,
    pre_lpg,
    post_lpg,
    post_lpg - pre_lpg AS lpg_impact
FROM pre_period
FULL OUTER JOIN post_period ON
    pre_period.country = post_period.country AND
    pre_period.region = post_period.region AND
    pre_period.income_level = post_period.income_level AND
    pre_period.subsidy_level = post_period.subsidy_level;