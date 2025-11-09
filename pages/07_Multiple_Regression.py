import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data
import plot_functions as pf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

st.set_page_config(page_title="Multiple Regression", page_icon="🧮", layout="wide")

# Load data
df = load_data()

st.title("🧮 Multiple Linear Regression")
st.markdown("Predicting `Profit` based on `Sales`, `Quantity`, and `Discount`.")

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

if filtered_df.shape[0] < 10:
    st.warning("Not enough data to run a regression model with the current filters. Please select 'All' for all filters.")
else:
    # --- 1. Prepare Data for Model ---
    features = ['Sales', 'Quantity', 'Discount']
    target = 'Profit'
    
    X = filtered_df[features]
    y = filtered_df[target]
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # --- 2. Run the Algorithm ---
    model = LinearRegression()
    model.fit(X_train, y_train)

    # --- 3. Evaluate the Model ---
    y_pred = model.predict(X_test)
    r_squared = r2_score(y_test, y_pred)
    coefficients = model.coef_
    intercept = model.intercept_

    # --- 4. Display Results ---
    st.subheader("Model Performance")
    st.metric("Model R-squared (R²)", f"{r_squared:.3f}")
    st.markdown(f"This means our model can explain **{r_squared*100:.1f}%** of the variance in `Profit` using these 3 features.")
    
    st.markdown("---")
    
    # --- 5. VISUALIZATION: Actual vs. Predicted ---
    st.subheader("Model Accuracy: Actual Profit vs. Predicted Profit")
    
    # Create a DataFrame for plotting
    plot_df = pd.DataFrame({'Actual Profit': y_test, 'Predicted Profit': y_pred})
    
    fig = px.scatter(
        plot_df, 
        x='Actual Profit', 
        y='Predicted Profit', 
        title='Actual vs. Predicted Profit'
    )
    # Add the "perfect fit" 45-degree line
    fig.add_trace(go.Scatter(
        x=[y_test.min(), y_test.max()], 
        y=[y_test.min(), y_test.max()], 
        mode='lines', 
        name='Perfect Fit',
        line=dict(color='red', dash='dash')
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("A perfect model would have all dots on the red 'Perfect Fit' line. This plot shows how well the model predicts profit.")

    # --- 6. Display Coefficients ---
    st.subheader("What Drives Profit? (Model Coefficients)")
    st.markdown("These numbers show how much `Profit` changes for a 1-unit increase in each feature, holding all others constant.")

    coeff_df = pd.DataFrame(
        coefficients,
        index=features,
        columns=['Coefficient (Impact on Profit)']
    )
    
    st.dataframe(
        coeff_df.style.format("${:.2f}").background_gradient(cmap='RdYlGn', axis=0),
        use_container_width=True
    )

    st.markdown(f"**Full Equation:** `Profit = ({coeff_df.loc['Sales'].values[0]:.2f} * Sales) + ({coeff_df.loc['Quantity'].values[0]:.2f} * Quantity) + ({coeff_df.loc['Discount'].values[0]:.2f} * Discount) + {intercept:.2f}`")