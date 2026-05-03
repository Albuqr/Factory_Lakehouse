import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import queries
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from queries import get_budget_variance

st.title("💰 Budget Variance Analysis")
st.markdown("---")

try:
    df = get_budget_variance()

    if df.empty:
        st.warning("⚠️ **Data Quality Issue**")
        st.info("""
        Budget variance tracking is currently unavailable due to missing supplier descriptions in the source transaction data.

        **Root Cause:** The DFC Excel sheet contains merged cells and null values in the description column, preventing proper categorization of transactions by cost center.

        **To Enable This Feature:**
        1. Clean the source Excel file (unmerge cells, fill descriptions)
        2. Update seed_supplier_lookup.csv with actual transaction descriptions
        3. Re-run dbt models

        **Current Status:** 2 of 3 dashboard pages are fully functional (SKU Economics and Equipment Status).
        """)
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Budget", f"R$ {df['budget_amount_brl'].sum():,.2f}")
        with col2:
            st.metric("Total Actual", f"R$ {df['actual_amount_brl'].sum():,.2f}")
        with col3:
            total_variance = df['variance_brl'].sum()
            st.metric("Total Variance", f"R$ {total_variance:,.2f}")

        st.markdown("---")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading budget data: {str(e)}")