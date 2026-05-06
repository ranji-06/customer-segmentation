import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("🧠 Customer Segmentation Dashboard")

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
    # Sample Dataset
    df = pd.DataFrame({
        "CustomerID": range(1, 101),
        "Age": [22,25,47,52,46,56,23,34,45,65]*10,
        "Annual Income": [15,16,17,18,19,20,30,35,40,60]*10,
        "Spending Score": [39,81,6,77,40,76,94,3,72,5]*10
    })

# -------------------------------
# SIDEBAR (SLICERS)
# -------------------------------
st.sidebar.header("🔍 Filters")

income_range = st.sidebar.slider(
    "Select Income Range",
    int(df["Annual Income"].min()),
    int(df["Annual Income"].max()),
    (int(df["Annual Income"].min()), int(df["Annual Income"].max()))
)

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

# Apply filters
df_filtered = df[
    (df["Annual Income"].between(income_range[0], income_range[1])) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# -------------------------------
# CLUSTERING
# -------------------------------
st.sidebar.subheader("⚙ Clustering Settings")

k = st.sidebar.slider("Select Number of Clusters (K)", 2, 6, 3)

X = df_filtered[["Annual Income", "Spending Score"]]

kmeans = KMeans(n_clusters=k, random_state=42)
df_filtered["Cluster"] = kmeans.fit_predict(X)

# -------------------------------
# KPI
# -------------------------------
st.subheader("📊 Overview")

col1, col2 = st.columns(2)
col1.metric("Total Customers", len(df_filtered))
col2.metric("Clusters Formed", k)

# -------------------------------
# CLUSTER VISUALIZATION
# -------------------------------
st.subheader("📈 Customer Segments")

fig = px.scatter(
    df_filtered,
    x="Annual Income",
    y="Spending Score",
    color="Cluster",
    size="Age",
    hover_data=["CustomerID"],
    title="Customer Segmentation"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# CLUSTER DISTRIBUTION
# -------------------------------
st.subheader("📊 Cluster Distribution")

cluster_count = df_filtered["Cluster"].value_counts().reset_index()
cluster_count.columns = ["Cluster", "Count"]

fig2 = px.bar(cluster_count, x="Cluster", y="Count", color="Cluster")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# INSIGHTS
# -------------------------------
st.subheader("🧠 Insights")

for i in range(k):
    cluster_data = df_filtered[df_filtered["Cluster"] == i]
    avg_income = cluster_data["Annual Income"].mean()
    avg_spend = cluster_data["Spending Score"].mean()

    st.write(f"Cluster {i}: Avg Income = {avg_income:.2f}, Avg Spending = {avg_spend:.2f}")

# -------------------------------
# DATA TABLE
# -------------------------------
st.subheader("📄 Data")
st.dataframe(df_filtered)