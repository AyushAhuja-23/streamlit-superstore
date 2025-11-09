import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
import plot_functions as pf
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

st.set_page_config(page_title="Product Affinity", page_icon="🛒", layout="wide")

# Load data
df = load_data()

st.title("🛒 Product Affinity (Association Rules)")
st.markdown("Find which sub-categories are most frequently purchased together in the same order.")

# --- Filters ---
st.sidebar.header("Filters")

year_choices = ["All"] + sorted(df['Order Year'].unique())
region_choices = ["All"] + sorted(df['Region'].unique())
category_choices = ["All"] + sorted(df['Category'].unique())

sel_year = st.sidebar.selectbox('Year', options=year_choices)
sel_region = st.sidebar.selectbox('Region', options=region_choices)
sel_category = st.sidebar.selectbox('Category', options=category_choices)

# --- Apply Filters ---
filtered_df = pf.apply_filters(df, sel_year, sel_region, sel_category, "All")

# --- Apriori Algorithm ---
st.subheader("Association Rules Model")

# 1. Prepare the "basket"
basket = filtered_df.groupby('Order ID')['Sub-Category'].apply(list).values.tolist()

if not basket:
    st.warning("No orders found for the selected filters.")
else:
    # 2. One-hot encode the data
    te = TransactionEncoder()
    te_ary = te.fit(basket).transform(basket)
    df_basket = pd.DataFrame(te_ary, columns=te.columns_)

    # 3. Run the Apriori algorithm
    try:
        frequent_itemsets = apriori(df_basket, min_support=0.01, use_colnames=True)
        
        # 4. Find the association rules
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
        
        rules = rules.sort_values(by='confidence', ascending=False)
        
        if rules.empty:
            st.warning("No significant product associations found for the current filters (min_support=1%).")
        else:
            
            # --- 5. FIX: Convert frozensets to strings for plotting ---
            # We create new columns for the hover data
            rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
            # --- END OF FIX ---

            st.subheader("Rule Visualization (Support vs. Confidence)")
            fig = px.scatter(
                rules,
                x="support",
                y="confidence",
                color="lift",
                size="lift",
                # Use the new string columns for hover data
                hover_data=['antecedents_str', 'consequents_str'], 
                color_continuous_scale="Viridis",
                title="Association Rule Strength (Support vs. Confidence)"
            )
            fig.update_layout(
                xaxis_title="Support (Frequency)",
                yaxis_title="Confidence (Reliability)"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Display the rules table
            st.subheader("Top Association Rules (Table)")
            
            # Use the same string columns for the table display
            rules_display = rules[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']]
            rules_display = rules_display.rename(columns={
                'antecedents_str': 'antecedents',
                'consequents_str': 'consequents'
            })

            st.dataframe(
                rules_display.style
                .format({'support': '{:.2%}', 'confidence': '{:.2%}', 'lift': '{:.2f}'}),
                use_container_width=True
            )
            
            st.markdown("""
            **How to Read This Table:**
            * **antecedents:** The product(s) a client has (IF...).
            * **consequents:** The product(s) the client is likely to buy (...THEN).
            * **confidence:** "If a client buys the antecedent, what is the % chance they also buy the consequent?"
            * **lift:** How much *more* likely are these to be bought together than by random chance? (A score > 1 is good).
            """)

    except Exception as e:
        st.error(f"An error occurred during the Apriori calculation. The filtered dataset may be too small or sparse. Error: {e}")