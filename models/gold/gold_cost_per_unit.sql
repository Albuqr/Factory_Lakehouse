WITH cost_per_unit AS (
    SELECT
        month_key,
        product_line,
        sku_name,
        planned_units,
        planned_cost_brl,
        ROUND(
            CASE WHEN planned_units = 0 THEN NULL
                 ELSE planned_cost_brl / planned_units
            END, 2
        ) AS cost_per_planned_unit_brl
    FROM {{ ref('silver_production_plan') }}
),

unit_price AS (
    SELECT
        sku_name,
        units_sold,
        revenue_brl,
        ROUND(
            CASE WHEN units_sold = 0 THEN NULL
                 ELSE revenue_brl / units_sold
            END, 2
        ) AS unit_price_brl
    FROM {{ source('bronze', 'bronze_synthetic_sales') }}
)

SELECT
    cpu.month_key,
    cpu.product_line,
    cpu.sku_name,
    cpu.planned_units,
    cpu.planned_cost_brl,
    cpu.cost_per_planned_unit_brl,
    up.units_sold,
    up.revenue_brl,
    up.unit_price_brl,
    ROUND(
        CASE WHEN cpu.cost_per_planned_unit_brl IS NULL THEN NULL
             ELSE up.unit_price_brl - cpu.cost_per_planned_unit_brl
        END, 2
    ) AS gross_margin_brl,
    ROUND(
        CASE WHEN up.unit_price_brl = 0 OR up.unit_price_brl IS NULL THEN NULL
             ELSE (up.unit_price_brl - cpu.cost_per_planned_unit_brl)
                  / up.unit_price_brl * 100
        END, 2
    ) AS gross_margin_pct
FROM cost_per_unit AS cpu
LEFT JOIN unit_price AS up ON cpu.sku_name = up.sku_name