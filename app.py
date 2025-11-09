import streamlit as st
from data_loader import load_data
import plot_functions as pf # pf = plot_functions

# Set page config (must be the first Streamlit command in the main file)
st.set_page_config(
    page_title="Superstore BI Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Load data (this will be cached by the decorator in data_loader.py)
df = load_data()

# --- Page Title ---
st.title("🚀 Superstore BI Dashboard: Overview")

# --- Filters ---
# These filters will apply to this page
st.sidebar.header("Overview Filters")

# Get unique values for filters and add "All"
year_choices = ["All"] + sorted(df['Order Year'].unique())
region_choices = ["All"] + sorted(df['Region'].unique())
category_choices = ["All"] + sorted(df['Category'].unique())
segment_choices = ["All"] + sorted(df['Segment'].unique())

# Create the select boxes in the sidebar
sel_year = st.sidebar.selectbox('Year', options=year_choices)
sel_region = st.sidebar.selectbox('Region', options=region_choices)
sel_category = st.sidebar.selectbox('Category', options=category_choices)
sel_segment = st.sidebar.selectbox('Segment', options=segment_choices)

# --- Apply Filters ---
# Import the filtering function from plot_functions.py
filtered_df = pf.apply_filters(df, sel_year, sel_region, sel_category, sel_segment)

# --- KPIs ---
# Import the KPI function
kpis = pf.compute_kpis(filtered_df)

# Display KPIs in columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${kpis['total_sales']:,.2f}")
col2.metric("Total Profit", f"${kpis['total_profit']:,.2f}")
col3.metric("Avg. Discount", f"{kpis['avg_discount']:.2%}")
col4.metric("Total Orders", f"{kpis['total_orders']:,}")

st.markdown("---")

# --- Charts ---
# Import the plotting functions
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(pf.fig_yearly_overview(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(pf.fig_monthly_sales(filtered_df), use_container_width=True)

st.plotly_chart(pf.fig_sales_by_region(filtered_df), use_container_width=True)