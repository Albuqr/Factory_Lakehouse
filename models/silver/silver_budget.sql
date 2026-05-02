SELECT
    cost_center,
    budget_amount_brl,
    CAST(month_key AS STRING) AS month_key
FROM {{ source('bronze', 'bronze_synthetic_budget') }}