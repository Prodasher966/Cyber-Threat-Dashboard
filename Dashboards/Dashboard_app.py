# dashboard_app.py
# Streamlit Dashboard for Global Cybersecurity Threat Intelligence
# Uses processed CSVs + ML severity prediction and full Streamlit UI

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models.prediction_utils import predict_severity

# ==============================
# Load preprocessed data
# ==============================
@st.cache_data
def load_data():
    df_main = pd.read_csv("data/processed_data.csv")
    country = pd.read_csv("data/Cyber_Threat_Dashboard/country_summary.csv")
    attack_type = pd.read_csv("data/attack_type_summary.csv")
    industry = pd.read_csv("data/industry_summary.csv")
    yearly = pd.read_csv("data/Cyber_Threat_Dashboard/yearly_trends.csv")
    source = pd.read_csv("data/attack_source_summary.csv")
    vuln = pd.read_csv("data/vulnerability_summary.csv")
    return df_main, country, attack_type, industry, yearly, source, vuln

# Load data
df_main, df_country, df_attack, df_industry, df_yearly, df_source, df_vuln = load_data()

# ==============================
# Streamlit UI Page Config
# ==============================
st.set_page_config(
    page_title="Cybersecurity Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
title_col1, title_col2 = st.columns([7, 1])
with title_col1:
    st.title("🛡️ Global Cybersecurity Threat Intelligence Dashboard (2015–2024)")
    st.caption("Data Source: Kaggle — Global Cybersecurity Threats Dataset")
with title_col2:
    st.image("https://cdn-icons-png.flaticon.com/512/4845/4845766.png", width=70)

# ==============================
# Sidebar Navigation
# ==============================
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio(
    "Go to Page:",
    ["Dashboard Overview", "Trends & Patterns", "ML Severity Prediction", "About Project"]
)

# Sidebar Filters
st.sidebar.header("🔎 Filters")
year_filter = st.sidebar.multiselect(
    "Select Year(s)",
    sorted(df_main["Year"].unique()),
    default=sorted(df_main["Year"].unique())
)

country_filter = st.sidebar.multiselect(
    "Select Country", df_main["Country"].unique(), default=None
)

# Apply Filters
filtered_df = df_main[df_main["Year"].isin(year_filter)]
if country_filter:
    filtered_df = filtered_df[filtered_df["Country"].isin(country_filter)]

# ========================================================
# PAGE 1 — DASHBOARD OVERVIEW
# ========================================================
if menu == "Dashboard Overview":
    st.subheader("📌 High-level KPIs")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", len(filtered_df))
    col2.metric("Total Financial Loss ($M)", round(filtered_df["Financial Loss (in Million $)"].sum(), 2))
    col3.metric("Total Affected Users", int(filtered_df["Number of Affected Users"].sum()))

    st.markdown("---")

    st.subheader("📊 Incidents by Country")
    fig_country = px.choropleth(
        df_country,
        locations="Country",
        locationmode="country names",
        color="Total_Incidents",
        title="Global Incident Distribution",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_country, use_container_width=True)

# ========================================================
# PAGE 2 — TRENDS & PATTERNS
# ========================================================
if menu == "Trends & Patterns":
    st.subheader("📈 Yearly Trends")
    fig_trend = px.line(
        df_yearly,
        x="Year",
        y="Total_Incidents",
        markers=True,
        title="Yearly Cyberattack Trend"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("📌 Attack Type Distribution")
    fig_attack = px.bar(
        df_attack,
        x="Attack Type",
        y="Total_Incidents",
        text_auto=True,
        title="Distribution of Attack Types"
    )
    st.plotly_chart(fig_attack, use_container_width=True)

    st.subheader("🏭 Most Targeted Industries")
    fig_industry = px.bar(
        df_industry,
        x="Target Industry",
        y="Total_Incidents",
        text_auto=True,
        title="Industry-wise Attack Frequency"
    )
    st.plotly_chart(fig_industry, use_container_width=True)

# ========================================================
# PAGE 3 — ML PREDICTION
# ========================================================
if menu == "ML Severity Prediction":
    st.subheader("🤖 Cyberattack Severity Prediction (ML Model)")

    with st.expander("Enter Attack Details for Prediction:"):
        col1, col2 = st.columns(2)

        country_in = col1.selectbox("Country", df_main["Country"].unique())
        year_in = col2.selectbox("Year", sorted(df_main["Year"].unique()))

        attack_in = col1.selectbox("Attack Type", df_main["Attack Type"].unique())
        industry_in = col2.selectbox("Target Industry", df_main["Target Industry"].unique())

        loss_in = col1.number_input("Financial Loss (Million $)", min_value=0.0, step=0.1)
        users_in = col2.number_input("Number of Affected Users", min_value=0, step=10)

        source_in = col1.selectbox("Attack Source", df_main["Attack Source"].unique())
        vuln_in = col2.selectbox("Security Vulnerability Type", df_main["Security Vulnerability Type"].unique())

        defense_in = col1.selectbox("Defense Mechanism Used", df_main["Defense Mechanism Used"].unique())
        resolution_in = col2.number_input("Incident Resolution Time (Hours)", min_value=1, step=1)

        if st.button("Predict Severity", type="primary"):
            input_payload = {
                "Country": country_in,
                "Year": year_in,
                "Attack Type": attack_in,
                "Target Industry": industry_in,
                "Financial Loss (in Million $)": loss_in,
                "Number of Affected Users": users_in,
                "Attack Source": source_in,
                "Security Vulnerability Type": vuln_in,
                "Defense Mechanism Used": defense_in,
                "Incident Resolution Time (in Hours)": resolution_in
            }

            severity = predict_severity(input_payload)
            st.success(f"Predicted Cyberattack Severity: **{severity}**")

# ========================================================
# PAGE 4 — ABOUT PROJECT
# ========================================================
if menu == "About Project":
    st.header("📘 Project Overview")
    st.write("""
        This dashboard provides a global analysis of cybersecurity incidents from 2015–2024.

        **Includes:**
        - Data preprocessing & cleaning
        - EDA summaries
        - Interactive visual dashboards
        - ML-based attack severity prediction

        Built using **Python, Streamlit, Plotly, and Scikit-Learn**.
    """)

# ==============================
# Footer
# ==============================
st.markdown("---")
st.caption("Developed by ProDasher • ML + Analytics + Visualization Dashboard")


# To Run Use : streamlit run dashboard_app.py

#Note: Fix needed in Incidents by Country and Global Industry Distribution and Trends Graph
#Prediction Model need Fix too (showing outcomes only based on no of users affected)