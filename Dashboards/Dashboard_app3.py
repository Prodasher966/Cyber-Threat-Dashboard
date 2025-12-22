import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==================================================
# PAGE CONFIG (Dark Theme Friendly)
# ==================================================
st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# GLOBAL STYLING (Dark Polish)
# ==================================================
# st.markdown(
#     """
#     <style>
#     .stMetric {
#         background-color: #111827;
#         padding: 15px;
#         border-radius: 12px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# ==================================================
# DATA LOADING
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv(Path("processed_data.csv"))
    df["Year"] = df["Year"].astype(int)
    return df


df = load_data()

# ==================================================
# FIX COLUMN NAMING
# ==================================================
df = df.rename(columns={
    "Attack Type": "Attack_Type",
    "Target Industry": "Industry",
    "Financial Loss (in Million $)": "Financial_Loss"
})

df["Country"] = df["Country"].str.strip()

# ==================================================
# MULTI-PAGE NAV (SIMPLE & CLEAN)
# ==================================================
page = st.sidebar.radio(
    "📂 Navigation",
    ["Overview", "Country Drilldown"]
)

# ==================================================
# COMMON FILTERS
# ==================================================
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filters")

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

selected_attack_types = st.sidebar.multiselect(
    "Select Attack Types",
    sorted(df["Attack_Type"].dropna().unique()),
    default=sorted(df["Attack_Type"].dropna().unique())
)

# ==================================================
# APPLY FILTERS
# ==================================================
df_filtered = df.copy()

df_filtered = df_filtered[
    (df_filtered["Year"] >= start_year) &
    (df_filtered["Year"] <= end_year)
]

if selected_attack_types:
    df_filtered = df_filtered[df_filtered["Attack_Type"].isin(selected_attack_types)]

# ==================================================
# PAGE: OVERVIEW
# ==================================================
if page == "Overview":

    st.title("🛡️ Cyber Threat Intelligence Dashboard")
    st.caption("Global overview of cybersecurity incidents")

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Incidents", len(df_filtered))
    c2.metric("Countries Affected", df_filtered["Country"].nunique())
    c3.metric("Industries Impacted", df_filtered["Industry"].nunique())
    c4.metric("Total Loss ($M)", f"{df_filtered['Financial_Loss'].sum():,.0f}")

    st.markdown("---")

    # Country Map (Click = Drilldown)
    st.subheader("🌍 Incidents by Country (Click to Drill Down)")

    country_counts = (
        df_filtered.groupby("Country")
        .size()
        .reset_index(name="Incidents")
    )

    fig_map = px.choropleth(
        country_counts,
        locations="Country",
        locationmode="country names",
        color="Incidents",
        color_continuous_scale="Reds"
    )

    selected = st.plotly_chart(fig_map, use_container_width=True)

    # Store selected country manually
    clicked_country = st.selectbox(
        "Select Country for Drilldown",
        sorted(df_filtered["Country"].unique())
    )

    st.session_state["selected_country"] = clicked_country

    st.markdown("---")

    # Financial Loss (LOG SCALE)
    st.subheader("💰 Financial Loss by Year (Log Scale)")
    loss_year = df_filtered.groupby("Year")["Financial_Loss"].sum().reset_index()

    fig_loss = px.bar(
        loss_year,
        x="Year",
        y="Financial_Loss",
        log_y=True,
        title="Log-scaled Financial Loss ($M)"
    )

    st.plotly_chart(fig_loss, use_container_width=True)

    # Download Filtered Data
    st.markdown("---")
    st.subheader("⬇️ Download Filtered Data")

    csv = df_filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        data=csv,
        file_name="filtered_cyber_threat_data.csv",
        mime="text/csv"
    )

# ==================================================
# PAGE: COUNTRY DRILLDOWN
# ==================================================
if page == "Country Drilldown":

    st.title("🔎 Country Drilldown Analysis")

    country = st.session_state.get(
        "selected_country",
        df_filtered["Country"].iloc[0]
    )

    st.subheader(f"Analysis for {country}")

    country_df = df_filtered[df_filtered["Country"] == country]

    c1, c2 = st.columns(2)
    c1.metric("Incidents", len(country_df))
    c2.metric("Total Loss ($M)", f"{country_df['Financial_Loss'].sum():,.0f}")

    st.markdown("---")

    # Industry Breakdown
    industry_breakdown = (
        country_df.groupby("Industry")
        .size()
        .reset_index(name="Incidents")
    )

    fig_ind = px.bar(
        industry_breakdown,
        x="Industry",
        y="Incidents",
        title="Industry Impact"
    )

    st.plotly_chart(fig_ind, use_container_width=True)

    # Attack Type Breakdown
    attack_breakdown = (
        country_df.groupby("Attack_Type")
        .size()
        .reset_index(name="Count")
    )

    fig_attack = px.pie(
        attack_breakdown,
        names="Attack_Type",
        values="Count",
        title="Attack Type Distribution"
    )

    st.plotly_chart(fig_attack, use_container_width=True)

    st.markdown("---")
    st.dataframe(country_df, use_container_width=True)
