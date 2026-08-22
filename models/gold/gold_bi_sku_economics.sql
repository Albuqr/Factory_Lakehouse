SELECT
    month_key,
    product_line,
    sku_name,
    planned_units,
    planned_cost_brl,
    units_sold,
    revenue_brl,
    gross_margin_brl

FROM {{ ref('gold_cost_per_unit') }}
