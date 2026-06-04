import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Company Insights",
    page_icon="🏢",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/Salary_Dataset_with_Extra_Features.csv")

df = load_data()

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

salary_col = "Salary"

df[salary_col] = (
    df[salary_col]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df[salary_col] = pd.to_numeric(
    df[salary_col],
    errors="coerce"
)

df = df.dropna(subset=[salary_col])

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Company Filters")

selected_companies = st.sidebar.multiselect(
    "Select Companies",
    sorted(df["Company Name"].dropna().unique()),
    default=sorted(df["Company Name"].dropna().unique())[:20]
)

filtered_df = df[
    df["Company Name"].isin(selected_companies)
]

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏢 Company Insights Dashboard")

st.markdown("""
Analyze company salary trends, ratings, hiring patterns,
and compare organizations across multiple metrics.
""")

st.divider()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_companies = filtered_df["Company Name"].nunique()

avg_salary = filtered_df[salary_col].mean()

avg_rating = filtered_df["Rating"].mean()

total_records = len(filtered_df)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    f"{total_companies:,}"
)

c2.metric(
    "Average Salary",
    f"₹{avg_salary:,.0f}"
)

c3.metric(
    "Average Rating",
    f"{avg_rating:.2f}"
)

c4.metric(
    "Employees Records",
    f"{total_records:,}"
)

st.divider()

# --------------------------------------------------
# TOP PAYING COMPANIES
# --------------------------------------------------

st.subheader("💰 Top Paying Companies")

top_salary = (
    filtered_df.groupby("Company Name")[salary_col]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    top_salary,
    x=salary_col,
    y="Company Name",
    orientation="h",
    title="Average Salary by Company"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# COMPANY RATINGS
# --------------------------------------------------

st.subheader("⭐ Company Ratings")

rating_df = (
    filtered_df.groupby("Company Name")["Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    rating_df,
    x="Rating",
    y="Company Name",
    orientation="h",
    title="Top Rated Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SALARY VS RATING
# --------------------------------------------------

st.subheader("📈 Salary vs Rating")

company_metrics = (
    filtered_df.groupby("Company Name")
    .agg({
        salary_col: "mean",
        "Rating": "mean"
    })
    .reset_index()
)

fig = px.scatter(
    company_metrics,
    x="Rating",
    y=salary_col,
    size=salary_col,
    hover_name="Company Name",
    title="Relationship Between Rating and Salary"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HIRING DISTRIBUTION
# --------------------------------------------------

st.subheader("👨‍💻 Job Role Distribution")

role_dist = (
    filtered_df["Job Roles"]
    .value_counts()
    .head(15)
    .reset_index()
)

role_dist.columns = ["Job Role", "Count"]

fig = px.bar(
    role_dist,
    x="Job Role",
    y="Count",
    title="Most Common Job Roles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# LOCATION PRESENCE
# --------------------------------------------------

st.subheader("🌍 Company Presence by Location")

location_dist = (
    filtered_df["Location"]
    .value_counts()
    .reset_index()
)

location_dist.columns = ["Location", "Count"]

fig = px.pie(
    location_dist,
    names="Location",
    values="Count",
    title="Location Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

st.subheader("🔥 Company Salary Heatmap")

heatmap_data = (
    filtered_df.pivot_table(
        values=salary_col,
        index="Company Name",
        columns="Job Roles",
        aggfunc="mean"
    )
)

fig = px.imshow(
    heatmap_data.fillna(0),
    aspect="auto",
    title="Salary by Company and Job Role"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# COMPANY COMPARISON
# --------------------------------------------------

st.subheader("⚖ Company Comparison")

comparison = (
    filtered_df.groupby("Company Name")
    .agg({
        salary_col: "mean",
        "Rating": "mean"
    })
    .sort_values(by=salary_col, ascending=False)
    .head(20)
    .reset_index()
)

fig = px.scatter(
    comparison,
    x="Rating",
    y=salary_col,
    color="Company Name",
    size=salary_col,
    hover_name="Company Name",
    title="Company Comparison Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# AUTOMATED INSIGHTS
# --------------------------------------------------

st.subheader("🧠 Company Insights")

best_company_salary = (
    filtered_df.groupby("Company Name")[salary_col]
    .mean()
    .idxmax()
)

best_company_rating = (
    filtered_df.groupby("Company Name")["Rating"]
    .mean()
    .idxmax()
)

highest_salary = (
    filtered_df.groupby("Company Name")[salary_col]
    .mean()
    .max()
)

st.success(f"""
### Key Findings

🏆 Highest Paying Company: **{best_company_salary}**

⭐ Highest Rated Company: **{best_company_rating}**

💰 Highest Average Salary: **₹{highest_salary:,.0f}**

📊 Companies Analyzed: **{total_companies:,}**

📈 Average Company Rating: **{avg_rating:.2f}**
""")

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------

with st.expander("View Company Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Company Data",
    csv,
    "company_insights.csv",
    "text/csv"
)
