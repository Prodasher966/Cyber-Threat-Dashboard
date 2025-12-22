"""
eda_visualizations.py
---------------------
Generates aggregated CSV summaries for the dashboard using processed_data.csv.
This script does NOT produce interactive charts (Streamlit will do that live).
"""

import pandas as pd
import os

# ================================
# 1. Load Processed Data
# ================================
def load_data(path="data/processed_data.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed data not found at {path}")

    df = pd.read_csv(path)
    return df


# ================================
# 2. Generate EDA Summary Tables
# ================================
def generate_country_summary(df):
    summary = df.groupby("Country").agg(
        Total_Incidents=("Year", "count"),
        Avg_Financial_Loss=("Financial Loss (in Million $)", "mean"),
        Total_Financial_Loss=("Financial Loss (in Million $)", "sum"),
        Avg_Affected_Users=("Number of Affected Users", "mean"),
    ).reset_index()

    return summary


def generate_attack_type_summary(df):
    summary = df.groupby("Attack Type").agg(
        Total_Incidents=("Year", "count"),
        Avg_Financial_Loss=("Financial Loss (in Million $)", "mean"),
        Total_Affected_Users=("Number of Affected Users", "sum"),
    ).reset_index()

    return summary


def generate_industry_summary(df):
    summary = df.groupby("Target Industry").agg(
        Total_Incidents=("Year", "count"),
        Total_Financial_Loss=("Financial Loss (in Million $)", "sum"),
        Avg_Resolution_Time=("Incident Resolution Time (in Hours)", "mean")
    ).reset_index()

    return summary


def generate_yearly_trends(df):
    summary = df.groupby("Year").agg(
        Total_Incidents=("Country", "count"),
        Total_Financial_Loss=("Financial Loss (in Million $)", "sum"),
        Total_Affected_Users=("Number of Affected Users", "sum"),
    ).reset_index()

    return summary


def generate_attack_source_summary(df):
    summary = df.groupby("Attack Source").agg(
        Total_Incidents=("Year", "count"),
        Total_Financial_Loss=("Financial Loss (in Million $)", "sum"),
    ).reset_index()

    return summary


def generate_vulnerability_summary(df):
    summary = df.groupby("Security Vulnerability Type").agg(
        Total_Incidents=("Year", "count"),
        Avg_Resolution_Time=("Incident Resolution Time (in Hours)", "mean")
    ).reset_index()

    return summary


# ================================
# 3. Save summaries as CSV
# ================================
def save_summary(df, filename):
    output_path = f"data/{filename}"
    df.to_csv(output_path, index=False)
    print(f"[Saved] {output_path}")


# ================================
# 4. Master function to run all
# ================================
def run_eda_exports():
    df = load_data()

    print("Generating summary tables...")

    country = generate_country_summary(df)
    attack_type = generate_attack_type_summary(df)
    industry = generate_industry_summary(df)
    yearly = generate_yearly_trends(df)
    source = generate_attack_source_summary(df)
    vuln = generate_vulnerability_summary(df)

    save_summary(country, "country_summary.csv")
    save_summary(attack_type, "attack_type_summary.csv")
    save_summary(industry, "industry_summary.csv")
    save_summary(yearly, "yearly_trends.csv")
    save_summary(source, "attack_source_summary.csv")
    save_summary(vuln, "vulnerability_summary.csv")

    print("EDA summary export completed.")


# ================================
# 5. Run script
# ================================
if __name__ == "__main__":
    run_eda_exports()
