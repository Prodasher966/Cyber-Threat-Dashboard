"""
prediction_utils.py
--------------------
Utility functions for making severity predictions using the trained model.
Loads:
- severity_model.pkl
- model_features.json

Provides:
- load_model_and_metadata()
- encode_input()
- predict_severity()
"""

import json
import joblib
import numpy as np
import pandas as pd


# =================================================
# 1. Load Model + Encoders
# =================================================
def load_model_and_metadata(
    model_path="models/severity_model.pkl",
    metadata_path="models/model_features.json"
):
    """Loads trained model and metadata (encoders + feature list)."""

    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        raise FileNotFoundError("ERROR: Trained ML model not found. Run model_training.py first.")

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("ERROR: Model metadata JSON missing.")

    encoders = metadata["label_encoders"]
    features = metadata["model_features"]

    return model, encoders, features


# =================================================
# 2. Encode a single user input row
# =================================================
def encode_input(input_dict, encoders):
    """
    Encodes categorical features according to the same LabelEncoders
    used during training.

    input_dict = {
        "Country": "USA",
        "Year": 2023,
        "Attack Type": "Ransomware",
        ...
    }
    """

    encoded_row = {}

    for key, value in input_dict.items():

        # If categorical → encode using training mappings
        if key in encoders:
            classes = encoders[key]

            if value not in classes:
                # Unknown category → safest fallback = most common category
                value = classes[0]

            encoded_value = classes.index(value)
            encoded_row[key] = encoded_value

        else:
            # Numerical → keep as is
            encoded_row[key] = value

    return pd.DataFrame([encoded_row])


# =================================================
# 3. Predict severity
# =================================================
def predict_severity(input_data):
    """
    input_data example:
    {
        "Country": "India",
        "Year": 2024,
        "Attack Type": "Phishing",
        "Target Industry": "Finance",
        "Financial Loss (in Million $)": 12.5,
        "Number of Affected Users": 5200,
        "Attack Source": "Unknown",
        "Security Vulnerability Type": "Weak Credentials",
        "Defense Mechanism Used": "Firewall",
        "Incident Resolution Time (in Hours)": 48
    }
    """

    # Load model + metadata
    model, encoders, features = load_model_and_metadata()

    # Encode the input
    encoded_df = encode_input(input_data, encoders)

    # Ensure column order matches training data
    encoded_df = encoded_df[features]

    # Predict (returns encoded labels)
    pred = model.predict(encoded_df)[0]

    # Decode severity ("Low", "Medium", "High")
    severity_labels = encoders["Severity"]
    decoded_label = severity_labels[pred]

    return decoded_label


# =================================================
# 4. Optional batch prediction helper
# =================================================
def predict_batch(df):
    """
    Input: DataFrame with same raw column names as processed_data.csv
    Output: DataFrame with added Severity Prediction column
    """

    model, encoders, features = load_model_and_metadata()

    encoded_rows = []

    for _, row in df.iterrows():
        encoded_rows.append(
            encode_input(row.to_dict(), encoders).iloc[0].to_dict()
        )

    encoded_df = pd.DataFrame(encoded_rows)
    encoded_df = encoded_df[features]

    preds = model.predict(encoded_df)

    severity_labels = encoders["Severity"]
    decoded_preds = [severity_labels[p] for p in preds]

    df["Predicted Severity"] = decoded_preds
    return df
