import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add parent directory to path to import queries
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from queries import get_equipment_status

st.title("🔧 Equipment Maintenance Status")
st.markdown("---")

try:
    df = get_equipment_status()

    if df.empty:
        st.warning("No equipment status data available")
    else:
        # Filters
        col1, col2 = st.columns(2)

        with col1:
            machine_types = ['All'] + sorted(df['machine_type'].unique().tolist())
            selected_type = st.selectbox("Machine Type", machine_types)

        with col2:
            prod_lines = ['All'] + sorted(df['production_line'].unique().tolist())
            selected_line = st.selectbox("Production Line", prod_lines)

        # Filter data
        filtered_df = df.copy()
        if selected_type != 'All':
            filtered_df = filtered_df[filtered_df['machine_type'] == selected_type]
        if selected_line != 'All':
            filtered_df = filtered_df[filtered_df['production_line'] == selected_line]

        # Status counts
        st.markdown("### Maintenance Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total = len(filtered_df)
            st.metric("Total Equipment", total)

        with col2:
            overdue = len(filtered_df[filtered_df['maintenance_status'] == 'OVERDUE'])
            st.metric("🔴 Overdue", overdue)

        with col3:
            due_soon = len(filtered_df[filtered_df['maintenance_status'] == 'DUE_SOON'])
            st.metric("🟡 Due Soon", due_soon)

        with col4:
            ok = len(filtered_df[filtered_df['maintenance_status'] == 'OK'])
            st.metric("🟢 OK", ok)

        st.markdown("---")

        # Status distribution chart
        st.markdown("### Status Distribution")
        status_counts = filtered_df['maintenance_status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']

        color_map = {
            'OVERDUE': '#ef4444',
            'DUE_SOON': '#eab308',
            'OK': '#22c55e'
        }

        fig = px.bar(
            status_counts,
            x='Status',
            y='Count',
            color='Status',
            color_discrete_map=color_map,
            title='Equipment by Maintenance Status'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Equipment table with color coding
        st.markdown("### Equipment Details")


        # Add color coding
        def color_status(val):
            if val == 'OVERDUE':
                return 'background-color: #fee2e2; color: #991b1b'
            elif val == 'DUE_SOON':
                return 'background-color: #fef3c7; color: #92400e'
            else:
                return 'background-color: #dcfce7; color: #166534'


        styled_df = filtered_df[['item_id', 'machine_type', 'production_line', 'next_due_date', 'days_until_due',
                                 'maintenance_status']].style.applymap(
            color_status,
            subset=['maintenance_status']
        )

        st.dataframe(styled_df, use_container_width=True)

        # Priority alerts
        if overdue > 0:
            st.error(f"⚠️ **URGENT:** {overdue} equipment item(s) overdue for maintenance")
            overdue_items = filtered_df[filtered_df['maintenance_status'] == 'OVERDUE'][
                ['item_id', 'machine_type', 'days_until_due']]
            st.dataframe(overdue_items, use_container_width=True)

except Exception as e:
    st.error(f"Error loading equipment status data: {str(e)}")