SELECT
    cost_center,
    budget_amount_brl,
    month_key
FROM {{ source('bronze', 'bronze_synthetic_budget') }}