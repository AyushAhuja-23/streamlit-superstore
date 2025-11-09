import streamlit as st
from data_loader import load_data
import plot_functions as pf

st.set_page_config(page_title="Dashboard", page_icon="🌎", layout="wide")

# Load data
df = load_data()

# --- Page Title ---
st.title("🌎 Profitability & Geographical Dashboard")

# --- Filters ---
st.sidebar.header("Dashboard Filters")

year_choices = ["All"] + sorted(df['Order Year'].unique())
region_choices = ["All"] + sorted(df['Region'].unique())
category_choices = ["All"] + sorted(df['Category'].unique())

sel_year = st.sidebar.selectbox('Year', options=year_choices)
sel_region = st.sidebar.selectbox('Region', options=region_choices)
sel_category = st.sidebar.selectbox('Category', options=category_choices)

# --- Apply Filters ---
filtered_df = pf.apply_filters(df, sel_year, sel_region, sel_category, "All")

# --- KPIs ---
kpis = pf.compute_kpis(filtered_df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${kpis['total_sales']:,.2f}")
col2.metric("Total Profit", f"${kpis['total_profit']:,.2f}")
col3.metric("Avg. Discount", f"{kpis['avg_discount']:.2%}")
col4.metric("Total Orders", f"{kpis['total_orders']:,}")

st.markdown("---")

# --- Charts ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(pf.fig_profit_vs_sales(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(pf.fig_profit_by_category(filtered_df), use_container_width=True)

st.plotly_chart(pf.fig_sales_by_state(filtered_df), use_container_width=True)