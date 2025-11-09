import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
import plot_functions as pf
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Customer Segmentation", page_icon="🤖", layout="wide")

# Load data
df = load_data()

st.title("🤖 Customer Segmentation (K-Means Clustering)")
st.markdown("Automatically find hidden customer groups based on their total sales and profit.")

# --- 1. Prepare Data for Clustering ---
df_customer = df.groupby('Customer Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).reset_index()

df_customer = df_customer.rename(columns={'Order ID': 'Total Orders'})

if df_customer.shape[0] < 10:
    st.warning("Not enough customer data to perform clustering.")
else:
    # --- 2. Normalize Data ---
    features = ['Sales', 'Profit', 'Total Orders']
    X = df_customer[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- 3. User Controls ---
    st.sidebar.header("Clustering Controls")
    k = st.sidebar.slider(
        "Select Number of Clusters (K)",
        min_value=2, 
        max_value=8, 
        value=4, 
        step=1
    )

    # --- 4. Run the Algorithm ---
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    kmeans.fit(X_scaled)
    
    df_customer['Cluster'] = kmeans.labels_.astype(str) 

    # --- 5. Visualize the Clusters ---
    st.subheader(f"Customer Segments (K={k})")
    
    fig = px.scatter(
        df_customer,
        x="Sales",
        y="Profit",
        color="Cluster",
        size="Total Orders",
        hover_name="Customer Name",
        hover_data={"Sales": ":.2f", "Profit": ":.2f", "Total Orders": True, "Cluster": True},
        title="Customer Segments (Sales vs. Profit)"
    )
    fig.update_layout(xaxis_title="Total Sales ($)", yaxis_title="Total Profit ($)")
    st.plotly_chart(fig, use_container_width=True)

    # --- 6. Analyze Cluster Centers ---
    st.subheader("Cluster Profiles")
    st.markdown("This table shows the 'average' customer in each segment. (Values are in their original scale.)")
    
    centers_scaled = kmeans.cluster_centers_
    centers_original = scaler.inverse_transform(centers_scaled)
    
    df_centers = pd.DataFrame(centers_original, columns=features)
    df_centers['Segment'] = [f"Segment {i}" for i in range(k)]
    
    st.dataframe(
        # --- THIS IS THE FIX ---
        df_centers.set_index('Segment').style.format("{:,.2f}").background_gradient(cmap='viridis'),
        use_container_width=True
    )
    
    st.markdown("""
    **How to Read This:**
    * Look for the segment with high `Sales` and high `Profit` (your **Ideal Customers**).
    * Look for the segment with high `Sales` but low/negative `Profit` (your **Unprofitable Customers**).
    * Look for the segment with low `Sales` and low `Profit` (your **Occasional Customers**).
    """)