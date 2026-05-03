import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add parent directory to path to import queries
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from queries import get_sku_economics

st.title("📊 SKU Economics")
st.markdown("---")

try:
    df = get_sku_economics()

    if df.empty:
        st.warning("No SKU economics data available")
    else:
        # Filters
        col1, col2 = st.columns(2)

        with col1:
            products = ['All'] + sorted(df['product_line'].unique().tolist())
            selected_product = st.selectbox("Product Line", products)

        with col2:
            months = ['All'] + sorted(df['month_key'].unique().tolist(), reverse=True)
            selected_month = st.selectbox("Month", months)

        # Filter data
        filtered_df = df.copy()
        if selected_product != 'All':
            filtered_df = filtered_df[filtered_df['product_line'] == selected_product]
        if selected_month != 'All':
            filtered_df = filtered_df[filtered_df['month_key'] == selected_month]

        # Metrics
        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_units = filtered_df['planned_units'].sum()
            st.metric("Total Planned Units", f"{total_units:,.0f}")

        with col2:
            total_cost = filtered_df['planned_cost_brl'].sum()
            st.metric("Total Planned Cost", f"R$ {total_cost:,.2f}")

        with col3:
            avg_cost_per_unit = filtered_df['cost_per_planned_unit_brl'].mean()
            st.metric("Avg Cost Per Unit", f"R$ {avg_cost_per_unit:.2f}")

        with col4:
            months_count = filtered_df['month_key'].nunique()
            st.metric("Months in View", f"{months_count}")

        st.markdown("---")

        # Chart - Cost per Unit over Time
        st.markdown("### Cost Per Unit Trend")

        chart_data = filtered_df.groupby(['month_key', 'product_line'])[
            'cost_per_planned_unit_brl'].mean().reset_index()

        fig = px.line(
            chart_data,
            x='month_key',
            y='cost_per_planned_unit_brl',
            color='product_line',
            title='Cost Per Planned Unit Over Time',
            labels={
                'month_key': 'Month',
                'cost_per_planned_unit_brl': 'Cost Per Unit (R$)',
                'product_line': 'Product'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Data table
        st.markdown("### Detailed Data")
        st.dataframe(
            filtered_df[
                ['month_key', 'product_line', 'planned_units', 'planned_cost_brl', 'cost_per_planned_unit_brl']],
            use_container_width=True
        )

        # Note about null sales data
        st.info(
            "ℹ️ **Note:** Sales data (units_sold, revenue_brl) is currently null because bronze_synthetic_sales uses monthly aggregates while production planning is daily. This is a known limitation of the synthetic data generation.")

except Exception as e:
    st.error(f"Error loading SKU economics data: {str(e)}")