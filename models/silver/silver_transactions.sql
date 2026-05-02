WITH parsed AS (
    SELECT
        ingestion_date,
        DATE_ADD(DATE '1899-12-30', INTERVAL CAST(`Data` AS INT64) DAY) AS transaction_date,
        CAST(`Descrição` AS STRING) AS dsc,
        `Crédito`,
        `Débito`,
        `Saldo`
    FROM {{ source('bronze', 'bronze_transactions') }}
)

SELECT
    bt.transaction_date,
    EXTRACT(YEAR FROM bt.transaction_date) AS year,
    FORMAT_DATE('%Y%m', bt.transaction_date) AS month_key,
    bt.dsc,
    sl.tax_id,
    sl.supplier_name,
    sl.category,
    bt.`Crédito`,
    bt.`Débito`,
    bt.`Saldo`,
    sl.tax_id IS NULL AS needs_review,
    CASE
        WHEN bt.`Crédito` IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS is_incoming

FROM parsed AS bt
LEFT JOIN {{ ref('seed_supplier_lookup') }} AS sl
    ON bt.dsc = sl.raw_string