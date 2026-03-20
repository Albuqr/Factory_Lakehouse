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
    sl.cnpj,
    ds.supplier_name,
    ds.category,
    bt.credit_brl,
    bt.debit_brl,
    bt.running_balance_brl,
    bt.source_month,
    sl.cnpj IS NULL AS needs_review,
    CASE
        WHEN bt.credit_brl IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS is_incoming

FROM parsed AS bt
LEFT JOIN {{ source('seeds', 'seed_supplier_lookup') }} AS sl
    ON bt.description = sl.raw_string
LEFT JOIN {{ source('seeds', 'seed_dim_suppliers') }} AS ds
    ON sl.cnpj = ds.cnpj