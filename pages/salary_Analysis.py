import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Salary Analysis",
    page_icon="💰",
    layout="wide"
)

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
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Filters")

locations = st.sidebar.multiselect(
    "Location",
    sorted(df["Location"].dropna().unique()),
    default=sorted(df["Location"].dropna().unique())
)

roles = st.sidebar.multiselect(
    "Job Role",
    sorted(df["Job Roles"].dropna().unique()),
    default=sorted(df["Job Roles"].dropna().unique())
)

filtered_df = df[
    (df["Location"].isin(locations))
    &
    (df["Job Roles"].isin(roles))
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("💰 Salary Analysis Dashboard")

st.markdown(
    "Comprehensive salary analysis across locations, job roles and companies."
)

st.divider()

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

avg_salary = filtered_df[salary_col].mean()
median_salary = filtered_df[salary_col].median()
max_salary = filtered_df[salary_col].max()
min_salary = filtered_df[salary_col].min()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Salary",
    f"₹{avg_salary:,.0f}"
)

c2.metric(
    "Median Salary",
    f"₹{median_salary:,.0f}"
)

c3.metric(
    "Highest Salary",
    f"₹{max_salary:,.0f}"
)

c4.metric(
    "Lowest Salary",
    f"₹{min_salary:,.0f}"
)

st.divider()

# ---------------------------------------------------
# SALARY DISTRIBUTION
# ---------------------------------------------------

st.subheader("📊 Salary Distribution")

fig = px.histogram(
    filtered_df,
    x=salary_col,
    nbins=50,
    marginal="box",
    title="Salary Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# TOP PAYING JOB ROLES
# ---------------------------------------------------

st.subheader("🏆 Highest Paying Job Roles")

role_salary = (
    filtered_df.groupby("Job Roles")[salary_col]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    role_salary,
    x=salary_col,
    y="Job Roles",
    orientation="h",
    title="Average Salary by Job Role"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# LOCATION VS SALARY
# ---------------------------------------------------

st.subheader("📍 Salary by Location")

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

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# SALARY BOXPLOT
# ---------------------------------------------------

st.subheader("📦 Salary Spread Across Locations")

fig = px.box(
    filtered_df,
    x="Location",
    y=salary_col,
    points="outliers",
    title="Salary Variations by Location"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# TOP PAYING COMPANIES
# ---------------------------------------------------

st.subheader("🏢 Top Paying Companies")

company_salary = (
    filtered_df.groupby("Company Name")[salary_col]
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
    title="Top 15 Highest Paying Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# HEATMAP
# ---------------------------------------------------

st.subheader("🔥 Salary Heatmap")

heatmap_data = (
    filtered_df.pivot_table(
        values=salary_col,
        index="Location",
        columns="Job Roles",
        aggfunc="mean"
    )
)

fig = px.imshow(
    heatmap_data,
    aspect="auto",
    title="Average Salary by Location and Job Role"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# VIOLIN PLOT
# ---------------------------------------------------

st.subheader("🎻 Salary Density")

fig = px.violin(
    filtered_df,
    x="Location",
    y=salary_col,
    box=True,
    title="Salary Density by Location"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Salary Insights")

highest_role = (
    filtered_df.groupby("Job Roles")[salary_col]
    .mean()
    .idxmax()
)

highest_city = (
    filtered_df.groupby("Location")[salary_col]
    .mean()
    .idxmax()
)

highest_company = (
    filtered_df.groupby("Company Name")[salary_col]
    .mean()
    .idxmax()
)

st.success(f"""
### Key Insights

💰 Highest Paying Role: **{highest_role}**

📍 Highest Paying Location: **{highest_city}**

🏢 Highest Paying Company: **{highest_company}**

📈 Average Salary: **₹{avg_salary:,.0f}**

📊 Median Salary: **₹{median_salary:,.0f}**
""")

# ---------------------------------------------------
# DATA DOWNLOAD
# ---------------------------------------------------

st.subheader("📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="salary_analysis.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------

with st.expander("View Raw Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
