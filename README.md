# Streamlit Superstore BI Dashboard

This is a multi-page interactive Business Intelligence (BI) dashboard for Superstore data, built entirely in Python using Streamlit and Plotly.

This project ingests, cleans, and analyzes sales and profit data, providing 10+ pages of in-depth analysis.

## 🚀 Features

* **Multi-Page Structure:** A clean, modular app where each analysis has its own page.
* **KPI Dashboards:** High-level overviews for Sales, Profit, and Orders.
* **Geographical Analysis:** A Plotly choropleth map showing profit by state.
* **Statistical Models:**
    * **Linear & Multiple Regression:** Analyzes the impact of `Discount`, `Sales`, and `Quantity` on `Profit`.
    * **Pareto Analysis (80/20 Rule):** Finds the "vital few" customers driving most of the profit.
* **Data Mining Models:**
    * **K-Means Clustering:** Automatically segments customers into "personas" (e.g., "Ideal Customers," "Unprofitable") based on their sales and profit.
    * **Apriori (Association Rules):** Finds which products are frequently purchased together ("Market Basket Analysis").
* **Forecasting & Advanced Analysis:**
    * **Time Series Forecasting:** Uses Holt-Winters to predict future sales.
    * **Cohort & Funnel Analysis:** Tracks customer retention and process drop-off.
    * **Dynamic OLAP:** A pivot table tool to build custom reports.

## 🛠️ Technology Stack

* **Streamlit:** Core web app framework.
* **Pandas:** For all data loading, cleaning, and manipulation.
* **Plotly Express:** For interactive visualizations.
* **Scikit-learn:** For K-Means clustering and Regression models.
* **Mlxtend:** For Apriori (association rules) model.
* **Statsmodels:** For time series forecasting.

## 🏃 How to Run Locally

1.  Clone this repository.
2.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  Place the `Superstore.csv` file inside a `data/` folder.
4.  Run the app from your terminal:
    ```bash
    streamlit run app.py
    ```