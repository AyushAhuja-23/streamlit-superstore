import streamlit as st
import pandas as pd
import numpy as np

# ---------------- US State Mapping ----------------
us_state_abbrev = {
    'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA',
    'Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC',
    'Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL',
    'Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA',
    'Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN',
    'Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV',
    'New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY',
    'North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR',
    'Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD',
    'Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA',
    'Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'
}

# ---------------- Load & Prepare Data ----------------
@st.cache_data # This decorator caches the data, so it only loads once.
def load_data(path="data/Superstore.csv"):
    try:
        df = pd.read_csv(path, encoding="latin1")
    except:
        # Fallback to create mock data if file is missing
        rng = pd.date_range("2020-01-01", periods=36, freq="M")
        df = pd.DataFrame({
            "Order Date": rng, "Ship Date": rng + pd.to_timedelta(np.random.randint(1,6,size=36), unit='D'),
            "Order ID": [f"ORD{i:04d}" for i in range(1, 37)],
            "Segment": np.random.choice(["Consumer","Corporate","Home Office"], size=36),
            "State": np.random.choice(["California","New York","Texas","Illinois","Pennsylvania"], size=36),
            "Region": np.random.choice(["West","East","Central","South"], size=36),
            "Category": np.random.choice(["Furniture","Office Supplies","Technology"], size=36),
            "Sales": np.round(np.random.uniform(20,1500,size=36),2),
            "Discount": np.round(np.random.choice([0.0,0.1,0.2,0.3], size=36),2),
            "Profit": np.round(np.random.uniform(-200,800,size=36),2),
        })

    df = df.drop_duplicates().reset_index(drop=True)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month Sort'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
    df['Delivery Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['State_Code'] = df['State'].map(us_state_abbrev).fillna(df['State'])
    return df