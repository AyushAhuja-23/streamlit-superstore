import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    _HAS_STATS = True
except:
    _HAS_STATS = False

# ---------------- KPI & Filter Logic ----------------
def compute_kpis(filtered_df):
    total_sales = float(filtered_df['Sales'].sum())
    total_profit = float(filtered_df['Profit'].sum())
    avg_discount = float(filtered_df['Discount'].mean()) if len(filtered_df) else 0.0
    total_orders = int(filtered_df['Order ID'].nunique())
    return {"total_sales": total_sales,"total_profit": total_profit,"avg_discount": avg_discount,"total_orders": total_orders}

# We pass the main DF here to avoid using a global
def apply_filters(df, year, region, category, segment):
    d = df.copy()
    if year != "All": d = d[d['Order Year']==int(year)]
    if region != "All": d = d[d['Region']==region]
    if category != "All": d = d[d['Category']==category]
    if segment != "All": d = d[d['Segment']==segment]
    return d

# ---------------- Plotly Charts ----------------
def fig_monthly_sales(filtered_df):
    if filtered_df.empty: return px.bar(title='No data')
    monthly = filtered_df.groupby('Order Month Sort', as_index=False).agg({'Sales':'sum'}).sort_values('Order Month Sort')
    fig = px.bar(monthly, x='Order Month Sort', y='Sales', title='Monthly Sales')
    fig.add_trace(go.Scatter(x=monthly['Order Month Sort'], y=monthly['Sales'], mode='lines+markers', name='Trend'))
    return fig

def fig_yearly_overview(filtered_df):
    yearly = filtered_df.groupby('Order Year', as_index=False).agg({'Sales':'sum','Profit':'sum'}).sort_values('Order Year')
    fig = make_subplots(specs=[[{"secondary_y": True}]] )
    fig.add_trace(go.Bar(x=yearly['Order Year'], y=yearly['Sales'], name='Sales'), secondary_y=False)
    fig.add_trace(go.Scatter(x=yearly['Order Year'], y=yearly['Profit'], name='Profit', mode='lines+markers'), secondary_y=True)
    fig.update_layout(title_text='Sales & Profit by Year')
    return fig

def fig_profit_vs_sales(filtered_df):
    if filtered_df.empty: return px.scatter(title='No data')
    return px.scatter(filtered_df, x='Sales', y='Profit', color='Region', hover_data=['Order ID','Customer Name','Sub-Category'], title='Profit vs Sales')

def fig_profit_by_category(filtered_df):
    if filtered_df.empty: return px.bar(title='No data')
    cat = filtered_df.groupby('Category', as_index=False).agg({'Profit':'sum','Sales':'sum'})
    cat['Profit Margin %'] = 100*cat['Profit']/cat['Sales'].replace(0,np.nan)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=cat['Category'], y=cat['Profit'], name='Profit'), secondary_y=False)
    fig.add_trace(go.Scatter(x=cat['Category'], y=cat['Profit Margin %'], name='Profit Margin %', mode='lines+markers'), secondary_y=True)
    fig.update_layout(title_text='Profit & Margin by Category')
    return fig

def fig_sales_by_state(filtered_df):
    if filtered_df.empty: return px.choropleth(title='No data')
    state_agg = filtered_df.groupby(['State', 'State_Code']).agg({'Profit': 'sum'}).reset_index()
    return px.choropleth(state_agg, locations='State_Code', locationmode='USA-states', color='Profit',
                         scope='usa', hover_name='State', color_continuous_scale='RdYlGn',
                         title='Profit by State (USA)')

def fig_sales_by_region(filtered_df):
    if filtered_df.empty: return px.treemap(title='No data')
    s = filtered_df.groupby('Region', as_index=False).agg({'Sales':'sum'})
    return px.treemap(s, path=['Region'], values='Sales', title='Sales by Region')

def fig_forecast(filtered_df, periods=6):
    monthly = filtered_df.groupby('Order Month Sort', as_index=False).agg({'Sales':'sum'}).set_index('Order Month Sort').asfreq('MS').fillna(0)
    if _HAS_STATS and len(monthly)>=6:
        try:
            model = ExponentialSmoothing(monthly['Sales'], seasonal='add', seasonal_periods=12)
            fit = model.fit(optimized=True)
            fcast = fit.forecast(periods)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly.index, y=monthly['Sales'], mode='lines+markers', name='Actual'))
            fig.add_trace(go.Scatter(x=fcast.index, y=fcast.values, mode='lines+markers', name='Forecast', line=dict(dash='dash')))
            return fig
        except: return px.line(monthly, y='Sales', title='Forecast failed')
    return px.line(monthly, y='Sales', title='Actual Sales')

def fig_top_customers(filtered_df, top_n=10):
    if filtered_df.empty: return px.bar(title='No data')
    cust = filtered_df.groupby('Customer Name', as_index=False).agg({'Profit':'sum'}).sort_values('Profit', ascending=False).head(top_n)
    return px.bar(cust, x='Customer Name', y='Profit', title=f'Top {top_n} Customers by Profit')

def fig_cohort_analysis(filtered_df):
    if filtered_df.empty: return px.imshow([[0]], title='No data')
    df_cohort = filtered_df.groupby(['Customer ID', filtered_df['Order Date'].dt.to_period('M')]).size().reset_index(name='Orders')
    cohort_pivot = df_cohort.pivot(index='Customer ID', columns='Order Date', values='Orders').fillna(0)
    cohort_pivot.columns = cohort_pivot.columns.astype(str)
    fig = px.imshow(cohort_pivot, color_continuous_scale='Viridis', text_auto=True, title='Cohort Analysis: Orders per Customer per Month')
    return fig

def fig_funnel_analysis(filtered_df):
    if filtered_df.empty: return px.funnel(title='No data')
    stages = ['Orders Placed','Items Shipped','Total Profit']
    orders = filtered_df['Order ID'].nunique()
    shipped = filtered_df[filtered_df['Delivery Days']>=0]['Order ID'].nunique()
    profit_stage = int(filtered_df['Profit'].sum())
    fig = go.Figure(go.Funnel(y=stages, x=[orders, shipped, profit_stage], textinfo="value+percent initial"))
    return fig

def fig_discount_heatmap(filtered_df):
    if filtered_df.empty: return px.imshow([[0]], title='No data')
    pivot = pd.pivot_table(filtered_df, index='Discount', columns='Category', values='Profit', aggfunc='sum', fill_value=0)
    fig = px.imshow(pivot, color_continuous_scale='RdYlGn', text_auto=True, title='Discount vs Profit Heatmap')
    return fig