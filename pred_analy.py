import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Predictive Analytics Dashboard", layout="wide")

st.title("📈 Predictive Analytics Using Historical Data")

# -------------------------------
# LOAD DATA
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV/Excel File", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    # Sample Historical Dataset
    dates = pd.date_range(start="2024-01-01", periods=100)

    df = pd.DataFrame({
        "Date": dates,
        "Sales": np.random.randint(1000, 5000, 100)
    })

# -------------------------------
# PREPROCESSING
# -------------------------------
df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")

# Convert dates into numeric values
df["Days"] = (df["Date"] - df["Date"].min()).dt.days

# -------------------------------
# SIDEBAR SLICERS
# -------------------------------
st.sidebar.header("🔍 Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

future_days = st.sidebar.slider(
    "Days to Predict",
    7,
    60,
    30
)

# Apply date filter
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["Date"] <= pd.to_datetime(end_date))
    ]

# -------------------------------
# MODEL TRAINING
# -------------------------------
X = filtered_df[["Days"]]
y = filtered_df["Sales"]

model = LinearRegression()
model.fit(X, y)

# Predictions on historical data
historical_predictions = model.predict(X)

# -------------------------------
# FUTURE PREDICTION
# -------------------------------
future_day_values = np.arange(
    filtered_df["Days"].max() + 1,
    filtered_df["Days"].max() + future_days + 1
).reshape(-1, 1)

future_sales = model.predict(future_day_values)

future_dates = pd.date_range(
    start=filtered_df["Date"].max() + pd.Timedelta(days=1),
    periods=future_days
)

future_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted Sales": future_sales
})

# -------------------------------
# KPIs
# -------------------------------
st.subheader("📊 Model Performance")

mae = mean_absolute_error(y, historical_predictions)
r2 = r2_score(y, historical_predictions)

col1, col2 = st.columns(2)

col1.metric("Mean Absolute Error", f"{mae:.2f}")
col2.metric("R² Score", f"{r2:.2f}")

# -------------------------------
# HISTORICAL TREND
# -------------------------------
st.subheader("📈 Historical Sales Trend")

fig1 = px.line(
    filtered_df,
    x="Date",
    y="Sales",
    title="Historical Sales"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# PREDICTION CHART
# -------------------------------
st.subheader("🔮 Future Sales Prediction")

fig2 = px.line(
    future_df,
    x="Date",
    y="Predicted Sales",
    title="Predicted Future Sales"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# COMBINED CHART
# -------------------------------
st.subheader("📊 Actual vs Predicted")

combined_fig = px.line()

combined_fig.add_scatter(
    x=filtered_df["Date"],
    y=filtered_df["Sales"],
    mode='lines',
    name='Actual Sales'
)

combined_fig.add_scatter(
    x=future_df["Date"],
    y=future_df["Predicted Sales"],
    mode='lines',
    name='Predicted Sales'
)

st.plotly_chart(combined_fig, use_container_width=True)

# -------------------------------
# DATA TABLES
# -------------------------------
st.subheader("📄 Historical Data")
st.dataframe(filtered_df)

st.subheader("📄 Predicted Data")
st.dataframe(future_df)

# -------------------------------
# DOWNLOAD PREDICTIONS
# -------------------------------
csv = future_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Prediction Report",
    data=csv,
    file_name='future_predictions.csv',
    mime='text/csv',
)