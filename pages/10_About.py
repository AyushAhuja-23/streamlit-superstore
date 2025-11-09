import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="centered")

st.title("ℹ️ About This Dashboard")

st.markdown("""
This Superstore BI Dashboard provides deep insights into sales, profit, discounts, customers, and geography.

### 🛠️ Technology
- **Framework:** Streamlit
- **Data:** Pandas
- **Plotting:** Plotly
- **Forecasting:** Statsmodels (Holt-Winters)

### 🏗️ Project Structure
This app is built using Streamlit's multi-page app feature.
- `app.py`: The main "Overview" page.
- `data_loader.py`: Handles all data loading and caching.
- `plot_functions.py`: Contains all Plotly chart definitions.
- `pages/`: This folder contains all other app pages.
""")