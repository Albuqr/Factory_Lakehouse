SELECT
COUNT(*)

FROM {{ ref('gold_bi_sku_economics') }}

HAVING COUNT(*) < 1