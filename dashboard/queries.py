from config import client, PROJECT_ID, DATASET_ID
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def get_budget_variance():
    query = f"""
    SELECT 
        month_key,
        cost_center,
        budget_amount_brl,
        actual_amount_brl,
        variance_brl,
        variance_pct,
        status_flag
    FROM `{PROJECT_ID}.{DATASET_ID}.gold_budget_vs_actual`
    ORDER BY month_key DESC, cost_center
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300)
def get_sku_economics():
    query = f"""
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
    FROM `{PROJECT_ID}.{DATASET_ID}.gold_cost_per_unit`
    ORDER BY month_key DESC, product_line
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300)
def get_equipment_status():
    query = f"""
    SELECT 
        item_id,
        machine_type,
        production_line,
        maintenance_date,
        service_interval_days,
        next_due_date,
        days_until_due,
        maintenance_status
    FROM `{PROJECT_ID}.{DATASET_ID}.gold_equipment_status`
    ORDER BY days_until_due ASC
    """
    return client.query(query).to_dataframe()