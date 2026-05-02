SELECT
   item_id,
   machine_type,
   production_line,
   service_interval_days
FROM {{ ref('seed_equipment_types') }}