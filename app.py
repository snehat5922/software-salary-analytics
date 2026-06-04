import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Software Salary Analytics Dashboard",
    page_icon="💼",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.kpi-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.insight-box {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #4F46E5;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/Salary_Dataset_with_Extra_Features.csv")

df = load_data()

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

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

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🔍 Filters")

location_filter = st.sidebar.multiselect(
    "Location",
    sorted(df["Location"].dropna().unique()),
    default=sorted(df["Location"].dropna().unique())
)

role_filter = st.sidebar.multiselect(
    "Job Role",
    sorted(df["Job Roles"].dropna().unique()),
    default=sorted(df["Job Roles"].dropna().unique())
)

filtered_df = df[
    (df["Location"].isin(location_filter))
    &
    (df["Job Roles"].isin(role_filter))
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("💼 Software Salary Analytics Dashboard")
st.markdown(
    "Interactive dashboard for salary trends, company insights, location analytics and job role comparisons."
)

st.divider()

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

total_records = len(filtered_df)

avg_salary = filtered_df[salary_col].mean()

max_salary = filtered_df[salary_col].max()

companies = filtered_df["Company Name"].nunique()

avg_rating = filtered_df["Rating"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Professionals", f"{total_records:,}")
c2.metric("Average Salary", f"₹{avg_salary:,.0f}")
c3.metric("Highest Salary", f"₹{max_salary:,.0f}")
c4.metric("Companies", f"{companies:,}")
c5.metric("Avg Rating", f"{avg_rating:.2f}")

st.divider()

# ---------------------------------------------------
# CHARTS ROW 1
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x=salary_col,
        nbins=40,
        title="Salary Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    company_salary = (
        filtered_df.groupby("Company Name")[salary_col]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        company_salary,
        x=salary_col,
        y="Company Name",
        orientation="h",
        title="Top Paying Companies"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# CHARTS ROW 2
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    role_salary = (
        filtered_df.groupby("Job Roles")[salary_col]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        role_salary,
        x="Job Roles",
        y=salary_col,
        title="Top Paying Job Roles"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.scatter(
        filtered_df,
        x="Rating",
        y=salary_col,
        color="Location",
        title="Company Rating vs Salary"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# CHARTS ROW 3
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.box(
        filtered_df,
        x="Location",
        y=salary_col,
        title="Salary Distribution by Location"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        filtered_df,
        names="Employment Status",
        title="Employment Type Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# TREEMAP
# ---------------------------------------------------

st.subheader("🌍 Salary Treemap")

fig = px.treemap(
    filtered_df,
    path=["Location", "Job Roles"],
    values=salary_col,
    color=salary_col
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# LOCATION ANALYTICS
# ---------------------------------------------------

st.subheader("📍 Location Analytics")

location_salary = (
    filtered_df.groupby("Location")[salary_col]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    location_salary,
    x="Location",
    y=salary_col,
    title="Average Salary by Location"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Automated Insights")

highest_role = (
    filtered_df.groupby("Job Roles")[salary_col]
    .mean()
    .idxmax()
)

highest_company = (
    filtered_df.groupby("Company Name")[salary_col]
    .mean()
    .idxmax()
)

highest_city = (
    filtered_df.groupby("Location")[salary_col]
    .mean()
    .idxmax()
)

st.success(
    f"""
### Key Findings

✅ Highest Paying Role: **{highest_role}**

✅ Highest Paying Company: **{highest_company}**

✅ Highest Paying Location: **{highest_city}**

✅ Average Salary: **₹{avg_salary:,.0f}**

✅ Total Companies Analyzed: **{companies:,}**
"""
)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Built using Streamlit • Plotly • Pandas • Salary Analytics Dashboard"
)
