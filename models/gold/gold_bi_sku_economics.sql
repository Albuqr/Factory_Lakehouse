SELECT
    month_key,
    product_line,
    sku_name,
    planned_units,
    planned_cost_brl,
    units_sold,
    revenue_brl,
    revenue_brl - (units_sold * (planned_cost_brl / planned_units)) AS gross_margin_total_brl
FROM {{ ref('gold_cost_per_unit') }}

