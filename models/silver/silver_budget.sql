WITH unpivoted AS (
    SELECT
        budget_year,
        cost_center,
        line_item,
        month,
        amount AS budget_amount_brl
    FROM {{ source('bronze', 'bronze_budget_monthly') }}
    UNPIVOT (
        amount FOR month IN (jan, feb, mar, apr, may, jun,
                             jul, aug, sep, oct, nov, dec)
    )
)

SELECT
    budget_year,
    cost_center,
    line_item,
    FORMAT_DATE('%Y%m', PARSE_DATE('%Y %b', CAST(budget_year AS STRING) || ' ' || month)) AS month_key,
    EXTRACT(MONTH FROM PARSE_DATE('%Y %b', CAST(budget_year AS STRING) || ' ' || month)) AS month_number,
    budget_amount_brl
FROM unpivoted