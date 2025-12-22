import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard",
    layout="wide"
)

st.title("🛡️ Cyber Threat Intelligence Dashboard")
st.markdown("Interactive analysis of global cybersecurity incidents")

# -----------------------------
# Data Loading
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(Path("data/processed_data.csv"))
    df["Year"] = df["Year"].astype(int)
    return df


df = load_data()

# -----------------------------
# FIX COLUMN NAMING (CRITICAL)
# -----------------------------
df = df.rename(columns={
    "Attack Type": "Attack_Type",
    "Target Industry": "Industry",
    "Financial Loss (in Million $)": "Financial_Loss"
})

# Clean country names for map safety
df["Country"] = df["Country"].str.strip()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    sorted(df["Country"].dropna().unique()),
    default=sorted(df["Country"].dropna().unique())
)

selected_industries = st.sidebar.multiselect(
    "Select Industries",
    sorted(df["Industry"].dropna().unique()),
    default=sorted(df["Industry"].dropna().unique())
)

selected_attack_types = st.sidebar.multiselect(
    "Select Attack Types",
    sorted(df["Attack_Type"].dropna().unique()),
    default=sorted(df["Attack_Type"].dropna().unique())
)

# -----------------------------
# Apply Filters (SINGLE SOURCE)
# -----------------------------
df_filtered = df.copy()

df_filtered = df_filtered[
    (df_filtered["Year"] >= start_year) &
    (df_filtered["Year"] <= end_year)
]

if selected_countries:
    df_filtered = df_filtered[df_filtered["Country"].isin(selected_countries)]

if selected_industries:
    df_filtered = df_filtered[df_filtered["Industry"].isin(selected_industries)]

if selected_attack_types:
    df_filtered = df_filtered[df_filtered["Attack_Type"].isin(selected_attack_types)]

# -----------------------------
# KPI Metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", len(df_filtered))
col2.metric("Countries Affected", df_filtered["Country"].nunique())
col3.metric("Industries Impacted", df_filtered["Industry"].nunique())
col4.metric(
    "Total Financial Loss ($M)",
    f"{df_filtered['Financial_Loss'].sum():,.0f}"
)

# -----------------------------
# Row 1: Geographic & Industry
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Incidents by Country")
    country_counts = (
        df_filtered.groupby("Country")
        .size()
        .reset_index(name="Incidents")
    )

    if not country_counts.empty:
        fig_country = px.choropleth(
            country_counts,
            locations="Country",
            locationmode="country names",
            color="Incidents",
            color_continuous_scale="Reds",
            title="Global Incident Distribution"
        )
        st.plotly_chart(fig_country, use_container_width=True)
    else:
        st.info("No data available")

with col2:
    st.subheader("🏭 Industry Distribution")
    industry_counts = (
        df_filtered.groupby("Industry")
        .size()
        .reset_index(name="Incidents")
    )

    fig_industry = px.pie(
        industry_counts,
        names="Industry",
        values="Incidents",
        title="Industry-wise Threat Distribution"
    )
    st.plotly_chart(fig_industry, use_container_width=True)

# -----------------------------
# Row 2: Attacks & Trends
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚔️ Attack Type Distribution")
    attack_counts = (
        df_filtered.groupby("Attack_Type")
        .size()
        .reset_index(name="Count")
    )

    fig_attack = px.bar(
        attack_counts,
        x="Attack_Type",
        y="Count",
        title="Attack Types"
    )
    st.plotly_chart(fig_attack, use_container_width=True)

with col2:
    st.subheader("📈 Yearly Incident Trends")
    yearly_trends = (
        df_filtered.groupby("Year")
        .size()
        .reset_index(name="Total Incidents")
    )

    fig_trend = px.line(
        yearly_trends,
        x="Year",
        y="Total Incidents",
        markers=True,
        title="Yearly Cybersecurity Incident Trends"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# Row 3: Financial Loss Analysis
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Financial Loss by Year")
    loss_by_year = (
        df_filtered.groupby("Year")["Financial_Loss"]
        .sum()
        .reset_index()
    )

    fig_loss_year = px.bar(
        loss_by_year,
        x="Year",
        y="Financial_Loss",
        title="Total Financial Loss per Year ($M)"
    )
    st.plotly_chart(fig_loss_year, use_container_width=True)

with col2:
    st.subheader("💸 Financial Loss by Industry")
    loss_by_industry = (
        df_filtered.groupby("Industry")["Financial_Loss"]
        .sum()
        .reset_index()
        .sort_values(by="Financial_Loss", ascending=False)
    )

    fig_loss_industry = px.bar(
        loss_by_industry,
        x="Industry",
        y="Financial_Loss",
        title="Financial Loss by Industry ($M)"
    )
    st.plotly_chart(fig_loss_industry, use_container_width=True)

# -----------------------------
# Row 4: Top 10 Rankings
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Countries by Incidents")
    top_countries = (
        df_filtered.groupby("Country")
        .size()
        .reset_index(name="Incidents")
        .sort_values(by="Incidents", ascending=False)
        .head(10)
    )

    fig_top_countries = px.bar(
        top_countries,
        x="Incidents",
        y="Country",
        orientation="h",
        title="Top 10 Countries"
    )
    st.plotly_chart(fig_top_countries, use_container_width=True)

with col2:
    st.subheader("🏭 Top 10 Industries by Incidents")
    top_industries = (
        df_filtered.groupby("Industry")
        .size()
        .reset_index(name="Incidents")
        .sort_values(by="Incidents", ascending=False)
        .head(10)
    )

    fig_top_industries = px.bar(
        top_industries,
        x="Incidents",
        y="Industry",
        orientation="h",
        title="Top 10 Industries"
    )
    st.plotly_chart(fig_top_industries, use_container_width=True)

# -----------------------------
# Data Preview
# -----------------------------
st.markdown("---")
st.subheader("📄 Filtered Data Preview")
st.dataframe(df_filtered, use_container_width=True)

#to run use streamlit run Dashboards/Dashboard_app2.py