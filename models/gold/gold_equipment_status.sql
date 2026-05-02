WITH latest_maintenance AS (
    SELECT
        item_id,
        maintenance_date,
        service_interval_days,
        ROW_NUMBER() OVER (
            PARTITION BY item_id
            ORDER BY maintenance_date DESC
        ) AS lm
    FROM {{ ref('silver_maintenance_logs') }}
),

next_due AS (
    SELECT
        item_id,
        maintenance_date,
        service_interval_days,
        CASE
            WHEN maintenance_date IS NULL THEN CURRENT_DATE
            ELSE CAST(DATE_ADD(maintenance_date, INTERVAL service_interval_days DAY) AS DATE)
        END AS next_due_date
    FROM latest_maintenance
    WHERE lm = 1
),

with_days AS (
    SELECT
        item_id,
        maintenance_date,
        service_interval_days,
        next_due_date,
        CASE
            WHEN maintenance_date IS NULL THEN 0
            ELSE DATE_DIFF(next_due_date, CURRENT_DATE, DAY)
        END AS days_until_due
    FROM next_due
)

SELECT
    wd.item_id,
    se.machine_type,
    se.production_line,
    wd.maintenance_date,
    wd.service_interval_days,
    wd.next_due_date,
    wd.days_until_due,
    CASE
        WHEN wd.days_until_due < 0 THEN 'OVERDUE'
        WHEN wd.days_until_due >= 0 AND wd.days_until_due <= 30 THEN 'DUE_SOON'
        ELSE 'OK'
    END AS maintenance_status
FROM with_days AS wd
LEFT JOIN {{ ref('silver_equipment') }} AS se ON wd.item_id = se.item_id