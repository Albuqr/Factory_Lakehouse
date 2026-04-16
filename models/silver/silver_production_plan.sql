WITH filtered_rows AS (
    SELECT
        CASE
        WHEN `0` = 'Pão de mel' THEN 'pao_de_mel'
        WHEN `0` = 'Trufa' THEN 'trufa'
        END AS product_line,
        `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`
    FROM {{ source('bronze', 'bronze_r_produto') }}
    WHERE `0` IN ('Pão de mel', 'Trufa')
    )


SELECT product_line, '202601' AS month_key, `1` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202602' AS month_key, `2` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202603' AS month_key, `3` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202604' AS month_key, `4` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202605' AS month_key, `5` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202606' AS month_key, `6` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202607' AS month_key, `7` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202608' AS month_key, `8` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202609' AS month_key, `9` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202610' AS month_key, `10` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202611' AS month_key, `11` AS planned_cost_brl FROM filtered_rows UNION ALL
SELECT product_line, '202612' AS month_key, `12` AS planned_cost_brl FROM filtered_rows