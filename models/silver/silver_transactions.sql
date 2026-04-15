WITH parsed AS (
    SELECT
        PARSE_DATE('%d/%m/%Y', transaction_date) AS transaction_date,
        description,
        credit_brl,
        debit_brl,
        running_balance_brl,
        source_month
    FROM {{ source('bronze', 'bronze_transactions') }}
)

SELECT
    bt.transaction_date,
    EXTRACT(YEAR FROM bt.transaction_date) AS year,
    FORMAT_DATE('%Y%m', bt.transaction_date) AS month_key,
    bt.description,
    sl.tax_id,
    sl.supplier_name,
    sl.category,
    bt.credit_brl,
    bt.debit_brl,
    bt.running_balance_brl,
    bt.source_month,
    sl.tax_id IS NULL AS needs_review,
    CASE
        WHEN bt.credit_brl IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS is_incoming

FROM parsed AS bt
LEFT JOIN {{ ref('seed_supplier_lookup') }} AS sl
    ON bt.description = sl.raw_string