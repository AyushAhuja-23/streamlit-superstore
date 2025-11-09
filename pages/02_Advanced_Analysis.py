import streamlit as st
from data_loader import load_data
import plot_functions as pf

st.set_page_config(page_title="Advanced Analysis", page_icon="🔍", layout="wide")

# Load data
df = load_data()

# --- Page Title ---
st.title("🔍 Advanced Analysis")

# --- Filters ---
st.sidebar.header("Analysis Filters")

year_choices = ["All"] + sorted(df['Order Year'].unique())
region_choices = ["All"] + sorted(df['Region'].unique())
category_choices = ["All"] + sorted(df['Category'].unique())
segment_choices = ["All"] + sorted(df['Segment'].unique())

sel_year = st.sidebar.selectbox('Year', options=year_choices)
sel_region = st.sidebar.selectbox('Region', options=region_choices)
sel_category = st.sidebar.selectbox('Category', options=category_choices)
sel_segment = st.sidebar.selectbox('Segment', options=segment_choices)
sel_top_n = st.sidebar.slider("Top N Customers", 1, 20, 10)

# --- Apply Filters ---
filtered_df = pf.apply_filters(df, sel_year, sel_region, sel_category, sel_segment)

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
    st.plotly_chart(pf.fig_top_customers(filtered_df, sel_top_n), use_container_width=True)
    st.plotly_chart(pf.fig_funnel_analysis(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(pf.fig_discount_heatmap(filtered_df), use_container_width=True)
    st.plotly_chart(pf.fig_cohort_analysis(filtered_df), use_container_width=True)