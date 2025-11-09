import streamlit as st
import plotly.express as px
from data_loader import load_data
import plot_functions as pf
from scipy import stats # Import for statistical calculations

st.set_page_config(page_title="Regression Analysis", page_icon="📉", layout="wide")

# Load data
df = load_data()

st.title("📉 Regression Analysis: Discount vs. Profit")
st.markdown("Does offering a higher discount lead to higher or lower profit?")

# --- Filters ---
st.sidebar.header("Filters")

year_choices = ["All"] + sorted(df['Order Year'].unique())
region_choices = ["All"] + sorted(df['Region'].unique())
category_choices = ["All"] + sorted(df['Category'].unique())

sel_year = st.sidebar.selectbox('Year', options=year_choices)
sel_region = st.sidebar.selectbox('Region', options=region_choices)
sel_category = st.sidebar.selectbox('Category', options=category_choices)

# --- Apply Filters ---
# We filter the data first based on user selection
filtered_df = pf.apply_filters(df, sel_year, sel_region, sel_category, "All")

# For this analysis, we only want to see data where a discount was given
df_analysis = filtered_df[filtered_df['Discount'] > 0]

if not df_analysis.empty:
    # --- Algorithm: Linear Regression ---
    # Plotly Express can run the 'ols' (Ordinary Least Squares) regression algorithm
    fig = px.scatter(
        df_analysis,
        x="Discount",
        y="Profit",
        title="Profit vs. Discount (where Discount > 0)",
        trendline="ols" # This line tells Plotly to run the regression
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Calculate and Display Stats ---
    st.subheader("Statistical Model Results")
    
    # Run the algorithm using scipy.stats to get the detailed numbers
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df_analysis['Discount'], 
        df_analysis['Profit']
    )
    r_squared = r_value**2
    
    col1, col2, col3 = st.columns(3)
    col1.metric("R-squared (R²)", f"{r_squared:.3f}")
    col2.metric("P-value", f"{p_value:.3g}")
    col3.metric("Slope", f"{slope:.2f}")
    
    st.markdown(f"**Regression Equation:** `Profit = {slope:.2f} * Discount + {intercept:.2f}`")
    
    st.markdown("### Interpretation")
    st.write(f"**R-squared:** {r_squared*100:.1f}% of the change in `Profit` can be explained by the `Discount`.")
    st.write(f"**Slope:** For every 1% increase in `Discount` (e.g., 0.01), the `Profit` changes by **${slope:.2f}**.")
    if p_value < 0.05:
        st.success("**The relationship is statistically significant (p < 0.05).**")
    else:
        st.error("**The relationship is not statistically significant (p >= 0.05).**")
else:
    st.warning("No data found with discounts greater than 0 for the selected filters.")