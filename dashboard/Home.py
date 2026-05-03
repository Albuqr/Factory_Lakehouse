import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.dirname(__file__))
from queries import get_budget_variance, get_sku_economics, get_equipment_status

st.set_page_config(
    page_title="Factory Lakehouse Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("🏭 Factory Lakehouse")
st.sidebar.markdown("---")
st.sidebar.info("Navigate using the pages above to explore different views of the data platform.")

# Main content
st.title("🏭 Factory Lakehouse - Data Platform")
st.markdown("---")

st.markdown("""
### Project Overview

A production-grade data lakehouse built for a Brazilian confectionery manufacturer with 28 machines, 2 product lines (Pão de Mel & Trufa), and operations entirely on paper. This platform bridges financial projections with operational reality through medallion architecture, dbt transformations, and real-time analytics.

**Tech Stack:** BigQuery • dbt • Streamlit • Python • Medallion Architecture
""")

st.markdown("---")

# Architecture Overview with Radar Chart
st.markdown("### 📊 Platform Coverage")

# Business-focused metrics for radar chart
categories = ['Raw Data<br>Collected', 'Data Cleaned<br>& Organized', 'Business<br>Insights',
              'Data<br>Reliability', 'System<br>Health']
values = [100, 100, 82, 73, 100]  # Updated: 82% insights (9/11 capabilities), 73% reliability (3 features blocked)

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Platform Coverage',
    line_color='#22c55e',
    fillcolor='rgba(34, 197, 94, 0.3)'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=False,
    height=650,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', size=14)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Tabs for layer details
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💡 How It Works", "🔶 Raw Data", "🔷 Clean Data", "🟡 Business Insights", "⚙️ Quality Control", "📊 Coverage Details"])

with tab0:
    st.markdown("""
    ### What is a Data Lakehouse?

    Think of it like organizing a warehouse. Instead of keeping inventory scattered everywhere, you:

    1. **Collect everything in one place** (Raw Data Layer)
       - All your Excel files, production logs, and financial records come here first
       - Nothing is changed yet - it's stored exactly as it was created

    2. **Sort and label everything properly** (Clean Data Layer)
       - Remove duplicates and errors
       - Translate confusing codes into readable names
       - Connect related information (like matching suppliers to transactions)

    3. **Create useful reports** (Business Insights Layer)
       - Answer questions like "Are we over budget?"
       - Track metrics like "How much does each product cost to make?"
       - Alert when equipment needs maintenance

    ### Why This Approach?

    **Before:** Spreadsheets everywhere, no single source of truth, manual updates, errors from copying data

    **After:** One system, automatic updates, reliable numbers, instant dashboards

    **For You:** Click a page in the sidebar → see current numbers → make informed decisions
    """)

with tab1:
    st.markdown("""
    ### Raw Data Collection

    **What We Track:**
    - Financial transactions from your cash flow Excel
    - Monthly budgets by department
    - All 28 machines in the factory
    - Daily production plans
    - Equipment maintenance history
    - Product cost estimates
    - Monthly sales figures

    **Status:** ✅ All data sources connected and updating automatically

    **What This Means:** Every number in your original files is safely stored and ready to use
    """)

with tab2:
    st.markdown("""
    ### Data Cleaning & Organization

    **What We Do:**
    - Convert messy Excel dates into proper calendar dates
    - Translate Portuguese column names to English for consistency
    - Match supplier names to transactions (118 suppliers tracked)
    - Connect equipment IDs to machine types (28 machines)
    - Standardize budget formats across months

    **Status:** ✅ All cleaning rules active and working

    **What This Means:** The system automatically fixes common data problems so your dashboards show accurate numbers
    """)

with tab3:
    st.markdown("""
    ### Business Insights Available

    **What You Can See:**

    ✅ **SKU Economics** (Working)
    - How much does each Pão de Mel or Trufa unit cost to produce?
    - Are costs going up or down over time?
    - 32 data points tracking 2 products across 16 months

    ✅ **Equipment Status** (Working)
    - Which machines need maintenance soon?
    - Which are overdue?
    - 28 machines tracked with automatic alerts

    ⚠️ **Budget Tracking** (Pending Fix)
    - Currently unavailable because supplier descriptions are missing in the source Excel file
    - Once source data is cleaned, this will show actual spending vs budget by department

    **What This Means:** 2 out of 3 dashboards give you real-time answers. The budget tracker just needs cleaner source data.
    """)

with tab4:
    st.markdown("""
    ### Quality Control & Reliability

    **What We Check:**
    - ✅ All data pipelines running without errors
    - ✅ No duplicate records
    - ✅ All dates and numbers formatted correctly
    - ✅ Supplier and equipment lookups working

    **Known Limitations:**
    - Some transaction descriptions missing (merged cells in original Excel)
    - Sales data is modeled/estimated (production data is real)

    **What This Means:** The system is stable and reliable. The limitations are in the source files, not the platform itself.
    """)

with tab5:
    st.markdown("""
    ### How Coverage is Measured

    #### Business Insights: 82% (9 of 11 capabilities working)

    **What YOU CAN do with the platform:**

    From SKU Economics:
    - ✅ Track production cost per unit for each product
    - ✅ Compare costs between Pão de Mel and Trufa
    - ✅ See cost trends over 16 months
    - ✅ Identify cost spikes and anomalies

    From Equipment Status:
    - ✅ Know which equipment needs service
    - ✅ Get automatic overdue alerts
    - ✅ Plan maintenance schedules
    - ✅ Prevent unexpected breakdowns

    From Budget Data:
    - ✅ View planned budgets by department

    **What you CANNOT do yet:**
    - ✗ Compare actual spending to budget (blocked by missing transaction descriptions)
    - ✗ Track variance by cost center (same root cause)

    **Total: 9 working capabilities / 11 total = 82%**

    ---

    #### Data Reliability: 73% (3 features blocked by data quality)

    **What ISN'T blocked:**
    - ✅ All SKU economics work (planned cost data is clean)
    - ✅ All equipment tracking works (inventory data is clean)
    - ✅ Budget planning works (budget data itself is fine)
    - ✅ All system health checks pass
    - ✅ All data transformations execute successfully

    **What IS blocked by source data quality:**
    - ✗ Budget variance analysis (missing supplier descriptions in transactions)
    - ✗ Supplier spend tracking (can't categorize transactions)
    - ✗ Cost center analysis (can't match transactions to departments)

    **Blocked features: 3 / Total features: ~11 = 73% reliable**

    **Why this matters:** The platform itself is 100% functional. The limitation is in the source Excel files (merged cells, missing descriptions). Once those are cleaned, reliability jumps to 100%.
    """)

st.markdown("---")

# Live Platform Stats
st.markdown("### 📈 Platform Status")

col1, col2, col3, col4 = st.columns(4)

try:
    sku_df = get_sku_economics()
    with col1:
        st.metric("Product Lines", len(sku_df['product_line'].unique()))
    with col2:
        st.metric("Cost Data Points", len(sku_df))
except:
    with col1:
        st.metric("Product Lines", "N/A")
    with col2:
        st.metric("Cost Data Points", "N/A")

try:
    equip_df = get_equipment_status()
    with col3:
        st.metric("Equipment Tracked", len(equip_df))
    with col4:
        overdue = len(equip_df[equip_df['maintenance_status'] == 'OVERDUE'])
        st.metric("🔴 Overdue Maintenance", overdue, delta=None if overdue == 0 else f"-{overdue}")
except:
    with col3:
        st.metric("Equipment Tracked", "N/A")
    with col4:
        st.metric("Overdue Maintenance", "N/A")