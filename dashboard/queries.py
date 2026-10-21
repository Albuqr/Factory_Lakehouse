from google.cloud import bigquery
from config import client, PROJECT_ID, DATASET_ID
import pandas as pd
import streamlit as st

# Tables below are resolved against this dataset, so the SQL carries no interpolated identifiers.
_JOB_CONFIG = bigquery.QueryJobConfig(default_dataset=f"{PROJECT_ID}.{DATASET_ID}")

@st.cache_data(ttl=300)
def get_budget_variance():
    query = """
    SELECT
        month_key,
        cost_center,
        budget_amount_brl,
        actual_amount_brl,
        variance_brl,
        variance_pct,
        status_flag
    FROM gold_budget_vs_actual
    ORDER BY month_key DESC, cost_center
    """
    return client.query(query, job_config=_JOB_CONFIG).to_dataframe()

@st.cache_data(ttl=300)
def get_sku_economics():
    query = """
    SELECT
        month_key,
        product_line,
        sku_name,
        planned_units,
        planned_cost_brl,
        cost_per_planned_unit_brl,
        units_sold,
        revenue_brl,
        unit_price_brl,
        gross_margin_brl,
        gross_margin_pct
    FROM gold_cost_per_unit
    ORDER BY month_key DESC, product_line
    """
    return client.query(query, job_config=_JOB_CONFIG).to_dataframe()

@st.cache_data(ttl=300)
def get_equipment_status():
    query = """
    SELECT
        item_id,
        machine_type,
        production_line,
        maintenance_date,
        service_interval_days,
        next_due_date,
        days_until_due,
        maintenance_status
    FROM gold_equipment_status
    ORDER BY days_until_due ASC
    """
    return client.query(query, job_config=_JOB_CONFIG).to_dataframe()
