WITH monthly_units AS (
    SELECT
        LOWER(sku) AS sku,
        FORMAT_DATE('%Y%m', production_date) AS month_key,
        SUM(units_produced) AS units
    FROM {{ source('bronze', 'bronze_production_plan') }}
    GROUP BY sku, month_key
)

SELECT
    CAST(pc.month_key AS STRING) AS month_key,
    pc.product_line,
    LOWER(pc.product_line) AS sku_name,
    mu.units AS planned_units,
    pc.planned_cost_brl
FROM {{ source('bronze', 'bronze_synthetic_planned_cost') }} AS pc
LEFT JOIN monthly_units AS mu
  ON pc.product_line = mu.sku
  AND CAST(pc.month_key AS STRING) = mu.month_key