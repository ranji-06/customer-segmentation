import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(page_title="Advanced Sales Dashboard", layout="wide")

st.title("📊 Advanced Sales & Revenue Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV/Excel File", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    # Sample Data
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=120),
        "Product": ["Product A", "Product B", "Product C", "Product D"] * 30,
        "Region": ["North", "South", "East", "West"] * 30,
        "Sales": [100, 200, 150, 300] * 30,
        "Revenue": [1000, 2000, 1500, 3000] * 30
    })

df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------
# SIDEBAR SLICERS
# -------------------------------
st.sidebar.header("🔍 Slicers / Filters")

# Product slicer
product = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Region slicer
region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Date slicer
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

# KPI slicer (extra feature 🔥)
kpi_option = st.sidebar.selectbox(
    "Select KPI",
    ["Sales", "Revenue"]
)

# -------------------------------
# APPLY FILTERS
# -------------------------------
df_filtered = df[
    (df["Product"].isin(product)) &
    (df["Region"].isin(region))
]

if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[
        (df_filtered["Date"] >= pd.to_datetime(start_date)) &
        (df_filtered["Date"] <= pd.to_datetime(end_date))
    ]

# -------------------------------
# KPIs
# -------------------------------
total_sales = df_filtered["Sales"].sum()
total_revenue = df_filtered["Revenue"].sum()

col1, col2 = st.columns(2)

col1.metric("💰 Total Sales", total_sales)
col2.metric("📈 Total Revenue", total_revenue)

# -------------------------------
# TREND CHART
# -------------------------------
st.subheader(f"📈 {kpi_option} Trend Over Time")

trend = df_filtered.groupby("Date")[kpi_option].sum().reset_index()

fig1 = px.line(trend, x="Date", y=kpi_option, markers=True)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# TOP PRODUCTS
# -------------------------------
st.subheader("🏆 Top Performing Products")

top_products = df_filtered.groupby("Product")[kpi_option].sum().reset_index()

fig2 = px.bar(
    top_products,
    x="Product",
    y=kpi_option,
    color="Product",
    text_auto=True
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# REGION ANALYSIS
# -------------------------------
st.subheader("🌍 Region-wise Distribution")

region_data = df_filtered.groupby("Region")[kpi_option].sum().reset_index()

fig3 = px.pie(
    region_data,
    names="Region",
    values=kpi_option,
    hole=0.4
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# DATA TABLE
# -------------------------------
st.subheader("📄 Filtered Data")
st.dataframe(df_filtered)

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------
csv = df_filtered.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv',
)