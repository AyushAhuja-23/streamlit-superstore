import streamlit as st
from data_loader import load_data
import plot_functions as pf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="OLAP", page_icon="🗃️", layout="wide")

# Load data
df = load_data()

# --- Page Title ---
st.title("🗃️ Dynamic OLAP Pivot Table")

# --- Filters ---
st.sidebar.header("OLAP Filters")

year_choices = ["All"] + sorted(df['Order Year'].unique())
region_choices = ["All"] + sorted(df['Region'].unique())

sel_year = st.sidebar.selectbox('Year', options=year_choices)
sel_region = st.sidebar.selectbox('Region', options=region_choices)

# --- Apply Filters ---
filtered_df = pf.apply_filters(df, sel_year, sel_region, "All", "All")

# --- OLAP Controls ---
st.markdown("### Pivot Table Controls")
col1, col2, col3 = st.columns(3)

olap_choices = ['Category','Sub-Category','Region','State', 'Segment']
val_choices = ['Sales','Profit','Quantity']
agg_choices = ['sum','mean','count']

with col1:
    sel_index = st.selectbox("Index (Rows)", options=olap_choices, index=0)
with col2:
    sel_cols = st.selectbox("Columns", options=olap_choices, index=2)
with col3:
    sel_agg = st.selectbox("Aggregation", options=agg_choices, index=0)
    
sel_val = st.selectbox("Values", options=val_choices, index=0)

if sel_index == sel_cols:
    st.error("Error: Index (Rows) and Columns cannot be the same. Please select different fields.")
else:
    # --- Generate Pivot ---
    st.markdown("---")
    st.subheader(f"{sel_agg.capitalize()} of {sel_val} by {sel_index} and {sel_cols}")
    
    pivot = pd.pivot_table(filtered_df, 
                           index=sel_index, 
                           columns=sel_cols, 
                           values=sel_val, 
                           aggfunc=sel_agg, 
                           fill_value=0)
    
    st.dataframe(pivot, use_container_width=True)
    
    # --- Pivot Heatmap ---
    fig_heatmap = px.imshow(pivot, 
                            text_auto=True, 
                            color_continuous_scale='Viridis',
                            title=f"Heatmap: {sel_agg.capitalize()} of {sel_val}")
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # --- Download ---
    csv = pivot.to_csv().encode('utf-8')
    st.download_button(
        label="Download Pivot Table as CSV",
        data=csv,
        file_name=f"{sel_val}_pivot.csv",
        mime="text/csv",
    )