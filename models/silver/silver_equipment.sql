SELECT
    be.item_id,
    be.equipment_name,
    be.brand,
    be.model,
    be.country_of_origin,
    be._ingested_at,
    se.machine_type,
    se.production_line
FROM {{ source('bronze', 'bronze_equipment') }} AS be
LEFT JOIN {{ source('seeds', 'seed_equipment_types') }} AS se
    ON be.item_id = se.item_id