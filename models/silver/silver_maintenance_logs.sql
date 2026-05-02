SELECT
    bml.machine_id AS item_id,
    bml.maintenance_date,
    seq.service_interval_days
FROM {{ source('bronze', 'bronze_maintenance_logs') }} AS bml
LEFT JOIN {{ ref('seed_equipment_types') }} AS seq
    ON bml.machine_id = seq.item_id