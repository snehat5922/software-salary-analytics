import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Location Analytics",
    page_icon="📍",
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
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Location Filters")

selected_locations = st.sidebar.multiselect(
    "Select Locations",
    sorted(df["Location"].dropna().unique()),
    default=sorted(df["Location"].dropna().unique())
)

selected_roles = st.sidebar.multiselect(
    "Select Job Roles",
    sorted(df["Job Roles"].dropna().unique()),
    default=sorted(df["Job Roles"].dropna().unique())
)

filtered_df = df[
    (df["Location"].isin(selected_locations))
    &
    (df["Job Roles"].isin(selected_roles))
]

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📍 Location Analytics Dashboard")

st.markdown("""
Analyze salary trends across locations, compare cities,
identify top-paying regions, and explore geographical insights.
""")

st.divider()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_locations = filtered_df["Location"].nunique()

avg_salary = filtered_df[salary_col].mean()

highest_salary = filtered_df[salary_col].max()

total_records = len(filtered_df)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Locations",
    f"{total_locations:,}"
)

c2.metric(
    "Average Salary",
    f"₹{avg_salary:,.0f}"
)

c3.metric(
    "Highest Salary",
    f"₹{highest_salary:,.0f}"
)

c4.metric(
    "Records",
    f"{total_records:,}"
)

st.divider()

# --------------------------------------------------
# LOCATION-WISE SALARY
# --------------------------------------------------

st.subheader("💰 Average Salary by Location")

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
    title="Average Salary by Location",
    text_auto=".0f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SALARY DISTRIBUTION
# --------------------------------------------------

st.subheader("📊 Salary Distribution Across Locations")

fig = px.box(
    filtered_df,
    x="Location",
    y=salary_col,
    points="outliers",
    title="Salary Spread by Location"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP JOB ROLES PER LOCATION
# --------------------------------------------------

st.subheader("👨‍💻 Most Common Job Roles")

role_count = (
    filtered_df.groupby("Job Roles")
    .size()
    .reset_index(name="Count")
    .sort_values("Count", ascending=False)
    .head(15)
)

fig = px.bar(
    role_count,
    x="Job Roles",
    y="Count",
    title="Top Job Roles Across Locations"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# LOCATION VS COMPANY COUNT
# --------------------------------------------------

st.subheader("🏢 Companies by Location")

company_count = (
    filtered_df.groupby("Location")["Company Name"]
    .nunique()
    .reset_index()
)

company_count.columns = [
    "Location",
    "Company Count"
]

fig = px.bar(
    company_count,
    x="Location",
    y="Company Count",
    title="Number of Companies by Location"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# LOCATION HEATMAP
# --------------------------------------------------

st.subheader("🔥 Salary Heatmap")

heatmap = (
    filtered_df.pivot_table(
        values=salary_col,
        index="Location",
        columns="Job Roles",
        aggfunc="mean"
    )
)

fig = px.imshow(
    heatmap.fillna(0),
    aspect="auto",
    title="Average Salary by Location and Job Role"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TREEMAP
# --------------------------------------------------

st.subheader("🌍 Location Treemap")

fig = px.treemap(
    filtered_df,
    path=["Location", "Job Roles"],
    values=salary_col,
    color=salary_col
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SUNBURST CHART
# --------------------------------------------------

st.subheader("☀️ Location Hierarchy")

fig = px.sunburst(
    filtered_df,
    path=["Location", "Employment Status", "Job Roles"],
    values=salary_col
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SCATTER ANALYSIS
# --------------------------------------------------

st.subheader("📈 Rating vs Salary by Location")

if "Rating" in filtered_df.columns:

    fig = px.scatter(
        filtered_df,
        x="Rating",
        y=salary_col,
        color="Location",
        hover_name="Company Name",
        title="Company Rating vs Salary"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.subheader("🧠 Location Insights")

best_location = (
    filtered_df.groupby("Location")[salary_col]
    .mean()
    .idxmax()
)

best_salary = (
    filtered_df.groupby("Location")[salary_col]
    .mean()
    .max()
)

most_companies = (
    filtered_df.groupby("Location")["Company Name"]
    .nunique()
    .idxmax()
)

st.success(f"""
### Key Findings

🏆 Highest Paying Location: **{best_location}**

💰 Average Salary There: **₹{best_salary:,.0f}**

🏢 Location with Most Companies: **{most_companies}**

📊 Locations Analysed: **{total_locations:,}**

📈 Overall Average Salary: **₹{avg_salary:,.0f}**
""")

# --------------------------------------------------
# LOCATION SUMMARY TABLE
# --------------------------------------------------

st.subheader("📋 Location Summary")

summary = (
    filtered_df.groupby("Location")
    .agg(
        Average_Salary=(salary_col, "mean"),
        Max_Salary=(salary_col, "max"),
        Companies=("Company Name", "nunique"),
        Records=("Location", "count")
    )
    .reset_index()
)

st.dataframe(
    summary,
    use_container_width=True
)

# --------------------------------------------------
# DOWNLOAD OPTION
# --------------------------------------------------

csv = summary.to_csv(index=False)

st.download_button(
    label="📥 Download Location Summary",
    data=csv,
    file_name="location_summary.csv",
    mime="text/csv"
)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------

with st.expander("View Raw Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )
