WITH actuals AS (
    SELECT
        month_key,
        cost_center,
        SUM(debit_brl) AS actual_amount_brl
    FROM {{ ref('silver_transactions') }}
    GROUP BY month_key, cost_center
),

budget AS (
    SELECT
        month_key,
        cost_center,
        budget_amount_brl
    FROM {{ ref('silver_budget') }}
),

variance AS (
    SELECT
        a.month_key,
        a.cost_center,
        b.budget_amount_brl,
        a.actual_amount_brl,
        a.actual_amount_brl - b.budget_amount_brl AS variance_brl
    FROM actuals AS a
    LEFT JOIN budget AS b
        ON a.month_key = b.month_key
        AND a.cost_center = b.cost_center
    WHERE b.budget_amount_brl > 0
)

SELECT
    month_key,
    cost_center,
    budget_amount_brl,
    actual_amount_brl,
    variance_brl,
    ROUND(
        CASE WHEN budget_amount_brl = 0 THEN NULL
             ELSE variance_brl / budget_amount_brl * 100
        END, 2
    ) AS variance_pct,
    CASE
        WHEN budget_amount_brl = 0 THEN 'grey'
        WHEN (variance_brl / budget_amount_brl * 100) < 10 THEN 'green'
        WHEN (variance_brl / budget_amount_brl * 100) <= 25 THEN 'yellow'
        ELSE 'red'
    END AS status_flag
FROM variance