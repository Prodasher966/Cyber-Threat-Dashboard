import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings("ignore")

def preprocess_data():
    # ===============================================================
    # 1. Load Raw Dataset
    # ===============================================================
    df = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")

    # ===============================================================
    # 2. Basic Cleaning
    # ===============================================================
    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Handle missing values (simple strategy)
    df["Financial Loss (in Million $)"].fillna(df["Financial Loss (in Million $)"].median(), inplace=True)
    df["Number of Affected Users"].fillna(df["Number of Affected Users"].median(), inplace=True)
    df["Incident Resolution Time (in Hours)"].fillna(df["Incident Resolution Time (in Hours)"].median(), inplace=True)

    # Fill categorical missing values
    for col in ["Attack Type", "Target Industry", "Attack Source", 
                "Security Vulnerability Type", "Defense Mechanism Used", "Country"]:
        df[col].fillna("Unknown", inplace=True)

    # ===============================================================
    # 3. Attack Severity Factor (Domain Knowledge)
    # ===============================================================

    severity_map = {
        "Ransomware": 1.0,
        "Zero-day": 1.0,
        "Malware": 0.6,
        "DDoS": 0.6,
        "Phishing": 0.4,
        "Social Engineering": 0.4,
        "Brute Force": 0.5,
        "Data Breach": 0.8,
        "SQL Injection": 0.7,
        "Man-in-the-middle": 0.7
    }

    def get_severity_factor(row):
        attack = row["Attack Type"]
        vuln = row["Security Vulnerability Type"]

        base = severity_map.get(attack, 0.3)
        vboost = 0.2 if "Zero" in vuln or "Misconfig" in vuln else 0.0

        return base + vboost

    df["attack_severity_factor"] = df.apply(get_severity_factor, axis=1)

    # ===============================================================
    # 4. Normalize Numeric Columns
    # ===============================================================
    numeric_cols = [
        "Financial Loss (in Million $)",
        "Number of Affected Users",
        "Incident Resolution Time (in Hours)"
    ]

    scaler = MinMaxScaler()
    df[[f"{col}_norm" for col in numeric_cols]] = scaler.fit_transform(df[numeric_cols])

    # ===============================================================
    # 5. Hybrid Risk Score
    # ===============================================================
    df["risk_score"] = (
        0.4 * df["Financial Loss (in Million $)_norm"] +
        0.3 * df["Number of Affected Users_norm"] +
        0.2 * df["Incident Resolution Time (in Hours)_norm"] +
        0.1 * df["attack_severity_factor"]
    )

    # ===============================================================
    # 6. KMeans Clustering for Severity Levels
    # ===============================================================
    kmeans_features = df[[
        "risk_score",
        "Financial Loss (in Million $)_norm",
        "Number of Affected Users_norm",
        "Incident Resolution Time (in Hours)_norm"
    ]]

    kmeans = KMeans(n_clusters=4, random_state=42)
    df["severity_cluster"] = kmeans.fit_predict(kmeans_features)

    # ===============================================================
    # 7. Convert Clusters → Severity Labels
    # ===============================================================
    # Get cluster centers sorted from low to high
    centers = kmeans.cluster_centers_.mean(axis=1)
    cluster_order = np.argsort(centers)

    severity_labels = {
        cluster_order[0]: "Low",
        cluster_order[1]: "Medium",
        cluster_order[2]: "High",
        cluster_order[3]: "Critical"
    }

    df["Severity"] = df["severity_cluster"].map(severity_labels)

    # ===============================================================
    # 8. Save Processed Data
    # ===============================================================
    df.to_csv("data/processed_data.csv", index=False)

    print("✔ Data preprocessing completed successfully!")
    print("✔ Processed file saved at: data/processed_data.csv")

    return df


if __name__ == "__main__":
    preprocess_data()
