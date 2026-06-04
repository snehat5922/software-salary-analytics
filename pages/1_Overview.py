import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
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
# HEADER
# --------------------------------------------------

st.title("📊 Dashboard Overview")

st.markdown(
    """
    Welcome to the Software Salary Analytics Dashboard.
    
    This dashboard provides an overview of salary trends,
    company performance, job role analytics and location-based insights.
    """
)

st.divider()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_records = len(df)
total_companies = df["Company Name"].nunique()
total_locations = df["Location"].nunique()
average_salary = df[salary_col].mean()
maximum_salary = df[salary_col].max()
average_rating = df["Rating"].mean()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Professionals",
    f"{total_records:,}"
)

c2.metric(
    "Companies",
    f"{total_companies:,}"
)

c3.metric(
    "Locations",
    f"{total_locations:,}"
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Average Salary",
    f"₹{average_salary:,.0f}"
)

c5.metric(
    "Highest Salary",
    f"₹{maximum_salary:,.0f}"
)

c6.metric(
    "Average Rating",
    f"{average_rating:.2f}"
)

st.divider()

# --------------------------------------------------
# TOP PAYING ROLES
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    role_salary = (
        df.groupby("Job Roles")[salary_col]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        role_salary,
        x=salary_col,
        y="Job Roles",
        orientation="h",
        title="Top 10 Highest Paying Job Roles"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    location_salary = (
        df.groupby("Location")[salary_col]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        location_salary,
        x="Location",
        y=salary_col,
        title="Top 10 Locations by Average Salary"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# COMPANY ANALYTICS
# --------------------------------------------------

st.subheader("🏢 Company Analytics")

company_salary = (
    df.groupby("Company Name")[salary_col]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    company_salary,
    x=salary_col,
    y="Company Name",
    orientation="h",
    title="Top Paying Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SALARY DISTRIBUTION
# --------------------------------------------------

st.subheader("💰 Salary Distribution")

fig = px.histogram(
    df,
    x=salary_col,
    nbins=50,
    title="Salary Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# EMPLOYMENT STATUS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        df,
        names="Employment Status",
        title="Employment Type Breakdown"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.scatter(
        df,
        x="Rating",
        y=salary_col,
        color="Location",
        title="Rating vs Salary"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# KEY INSIGHTS
# --------------------------------------------------

st.subheader("🧠 Executive Insights")

highest_role = (
    df.groupby("Job Roles")[salary_col]
    .mean()
    .idxmax()
)

highest_location = (
    df.groupby("Location")[salary_col]
    .mean()
    .idxmax()
)

highest_company = (
    df.groupby("Company Name")[salary_col]
    .mean()
    .idxmax()
)

st.info(
    f"""
### Key Findings

📌 Highest Paying Role: **{highest_role}**

📌 Highest Paying Company: **{highest_company}**

📌 Highest Paying Location: **{highest_location}**

📌 Average Salary Across Dataset: **₹{average_salary:,.0f}**

📌 Total Companies Analysed: **{total_companies:,}**
"""
)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(100),
    use_container_width=True
)
