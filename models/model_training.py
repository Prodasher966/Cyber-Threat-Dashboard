"""
model_training.py
-----------------
Trains a machine learning model to predict cyberattack severity.
Outputs:
- severity_model.pkl
- model_features.json
- encoded_training_data.csv (optional)
"""

import pandas as pd
import os
import json
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


# =================================================
# 1. Load processed data
# =================================================
def load_data(path="data/processed_data.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed data not found at {path}")

    df = pd.read_csv(path)
    return df


# =================================================
# 2. Create Severity Label (Quantile-based)
# =================================================
def add_severity_label(df):
    """
    Creates severity labels using quantiles (balanced classes):
        Low    = bottom 33%
        Medium = mid 33%
        High   = top 33%
    """

    q1 = df["Number of Affected Users"].quantile(0.33)
    q2 = df["Number of Affected Users"].quantile(0.66)

    df["Severity"] = pd.cut(
        df["Number of Affected Users"],
        bins=[-1, q1, q2, float("inf")],
        labels=["Low", "Medium", "High"]
    )

    print(f"\nSeverity thresholds:")
    print(f"Low     <= {q1:.2f}")
    print(f"Medium  <= {q2:.2f}")
    print(f"High    >  {q2:.2f}\n")

    return df


# =================================================
# 3. Encode categorical columns
# =================================================
def encode_categoricals(df):
    categorical_cols = [
        "Country",
        "Attack Type",
        "Target Industry",
        "Attack Source",
        "Security Vulnerability Type",
        "Defense Mechanism Used",
        "Severity"
    ]

    encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le.classes_.tolist()

    return df, encoders


# =================================================
# 4. Train Machine Learning Model
# =================================================
def train_model(df):
    features = [
        "Country", "Year", "Attack Type", "Target Industry",
        "Financial Loss (in Million $)", "Number of Affected Users",
        "Attack Source", "Security Vulnerability Type",
        "Defense Mechanism Used", "Incident Resolution Time (in Hours)"
    ]

    X = df[features]
    y = df["Severity"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=14,
        min_samples_split=4,
        random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\n===== Model Performance =====")
    print(classification_report(y_test, y_pred))

    return model, features


# =================================================
# 5. Save Model + Metadata
# =================================================
def save_outputs(model, encoders, features):
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/severity_model.pkl")
    print("[Saved] Cyber_Threat_Dashboard/severity_model.pkl")

    metadata = {
        "label_encoders": encoders,
        "model_features": features
    }

    with open("models/model_features.json", "w") as f:
        json.dump(metadata, f, indent=4)
    print("[Saved] models/model_features.json")


# =================================================
# 6. Optional: Save encoded training data
# =================================================
def save_encoded_training_data(df):
    df.to_csv("data/encoded_training_data.csv", index=False)
    print("[Saved] data/encoded_training_data.csv")


# =================================================
# 7. Master Function
# =================================================
def run_model_training():

    print("Loading cleaned data...")
    df = load_data()

    print("Assigning severity labels (quantile-based)...")
    df = add_severity_label(df)

    print("Encoding categorical columns...")
    df, encoders = encode_categoricals(df)

    print("Training model...")
    model, features = train_model(df)

    print("Saving model + metadata...")
    save_outputs(model, encoders, features)

    save_encoded_training_data(df)

    print("\nModel training completed successfully!")


# =================================================
# 8. Run
# =================================================
if __name__ == "__main__":
    run_model_training()
