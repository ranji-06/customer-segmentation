import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Data Cleaning Automation", layout="wide")

st.title("🧹 Data Cleaning & Reporting Automation")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# -------------------------------
# SAMPLE DATA IF NO FILE
# -------------------------------
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    # Sample messy dataset
    df = pd.DataFrame({
        "Name": ["John", "Alice", "Bob", None, "John"],
        "Age": [25, 30, None, 22, 25],
        "Salary": [50000, None, 45000, 40000, 50000],
        "Department": ["HR", "IT", "Finance", None, "HR"]
    })

# -------------------------------
# ORIGINAL DATA
# -------------------------------
st.subheader("📄 Original Dataset")
st.dataframe(df)

# -------------------------------
# SIDEBAR OPTIONS
# -------------------------------
st.sidebar.header("⚙ Cleaning Options")

remove_duplicates = st.sidebar.checkbox("Remove Duplicates", True)

fill_missing = st.sidebar.selectbox(
    "Handle Missing Values",
    ["None", "Fill with Mean", "Fill with Median", "Fill with Mode"]
)

# -------------------------------
# CLEANING PROCESS
# -------------------------------
cleaned_df = df.copy()

# Remove duplicates
duplicates_removed = 0

if remove_duplicates:
    duplicates_removed = cleaned_df.duplicated().sum()
    cleaned_df = cleaned_df.drop_duplicates()

# Handle missing values
missing_before = cleaned_df.isnull().sum().sum()

if fill_missing == "Fill with Mean":
    numeric_cols = cleaned_df.select_dtypes(include='number').columns
    cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(
        cleaned_df[numeric_cols].mean()
    )

elif fill_missing == "Fill with Median":
    numeric_cols = cleaned_df.select_dtypes(include='number').columns
    cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(
        cleaned_df[numeric_cols].median()
    )

elif fill_missing == "Fill with Mode":
    for col in cleaned_df.columns:
        cleaned_df[col] = cleaned_df[col].fillna(
            cleaned_df[col].mode()[0]
        )

missing_after = cleaned_df.isnull().sum().sum()

# -------------------------------
# KPI METRICS
# -------------------------------
st.subheader("📊 Cleaning Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Missing Values Before", int(missing_before))
col2.metric("Missing Values After", int(missing_after))
col3.metric("Duplicates Removed", int(duplicates_removed))

# -------------------------------
# CLEANED DATA
# -------------------------------
st.subheader("✅ Cleaned Dataset")
st.dataframe(cleaned_df)

# -------------------------------
# REPORT VISUALIZATION
# -------------------------------
st.subheader("📈 Data Visualization")

numeric_columns = cleaned_df.select_dtypes(include='number').columns

if len(numeric_columns) > 0:

    selected_column = st.selectbox(
        "Select Numeric Column",
        numeric_columns
    )

    fig = px.histogram(
        cleaned_df,
        x=selected_column,
        title=f"{selected_column} Distribution",
        nbins=20
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# NULL VALUE REPORT
# -------------------------------
st.subheader("📋 Missing Value Report")

null_report = pd.DataFrame({
    "Column": cleaned_df.columns,
    "Missing Values": cleaned_df.isnull().sum().values
})

st.dataframe(null_report)

# -------------------------------
# DOWNLOAD CLEANED FILE
# -------------------------------
csv = cleaned_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Cleaned Data",
    data=csv,
    file_name='cleaned_dataset.csv',
    mime='text/csv',
)

# -------------------------------
# AUTOMATED INSIGHTS
# -------------------------------
st.subheader("🧠 Automated Insights")

st.write(f"✔ Dataset contains {cleaned_df.shape[0]} rows and {cleaned_df.shape[1]} columns.")

st.write(f"✔ Removed {duplicates_removed} duplicate rows.")

st.write(f"✔ Remaining missing values: {missing_after}")