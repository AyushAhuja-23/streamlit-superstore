import streamlit as st
from data_loader import load_data
import plot_functions as pf

st.set_page_config(page_title="Forecasting", page_icon="🔮", layout="wide")

# Load data
df = load_data()

# --- Page Title ---
st.title("🔮 Sales Forecasting")

# --- Filters ---
st.sidebar.header("Forecast Filters")

year_choices = ["All"] + sorted(df['Order Year'].unique())
region_choices = ["All"] + sorted(df['Region'].unique())
category_choices = ["All"] + sorted(df['Category'].unique())

sel_year = st.sidebar.selectbox('Year', options=year_choices)
sel_region = st.sidebar.selectbox('Region', options=region_choices)
sel_category = st.sidebar.selectbox('Category', options=category_choices)
sel_periods = st.sidebar.slider("Forecast Periods (Months)", 1, 12, 6)

# --- Apply Filters ---
filtered_df = pf.apply_filters(df, sel_year, sel_region, sel_category, "All")

# --- Charts ---
st.subheader("Sales Forecast (Holt-Winters Model)")
st.plotly_chart(pf.fig_forecast(filtered_df, sel_periods), use_container_width=True)

st.subheader("Actual Monthly Sales (for context)")
st.plotly_chart(pf.fig_monthly_sales(filtered_df), use_container_width=True)