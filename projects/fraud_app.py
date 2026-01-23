import streamlit as st
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import joblib
import json

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Insurance Fraud Risk Prediction",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Insurance Claim Fraud Risk Prediction")
st.markdown(
    """
This application predicts **fraud risk score** for insurance claims using a
**CatBoost model with optimized threshold**.  
The model is designed to support **claim screening and investigation prioritization**.
"""
)

st.divider()

# ===============================
# Load Model, Cat Features & Threshold
# ===============================
@st.cache_resource
def load_model():
    model = CatBoostClassifier()
    model.load_model("projects/models/catboost_fraud_model.cbm")
    return model

@st.cache_resource
def load_cat_features():
    return joblib.load("projects/models/cat_features.pkl")

@st.cache_data
def load_threshold():
    with open("projects/models/fraud_config.json") as f:
        return json.load(f)["threshold"]

model = load_model()
cat_features = load_cat_features()
THRESHOLD = load_threshold()

# ===============================
# Upload Data
# ===============================
st.subheader("📤 Upload Claim Data")

uploaded_file = st.file_uploader(
    "Upload CSV file (insurance claim data)",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Data uploaded successfully!")
    st.write("Preview of uploaded data:")
    st.dataframe(df.head())

    # ===============================
    # Validate categorical columns
    # ===============================
    missing_cat_cols = [c for c in cat_features if c not in df.columns]

    if missing_cat_cols:
        st.error(
            f"Missing categorical columns required by the model: {missing_cat_cols}"
        )
        st.stop()

    # ===============================
    # Prediction
    # ===============================
    st.subheader("🔍 Fraud Risk Scoring")

    fraud_prob = model.predict_proba(
        df,
        cat_features=cat_features
    )[:, 1]

    df["fraud_risk_score"] = fraud_prob

    # ===============================
    # Fraud Prediction using OPTIMIZED THRESHOLD
    # ===============================
    df["fraud_prediction"] = (df["fraud_risk_score"] >= THRESHOLD).astype(int)

    # ===============================
    # Risk Classification
    # ===============================
    def risk_category(score):
        if score < 0.3:
            return "Low Risk"
        elif score < THRESHOLD:
            return "Medium Risk"
        else:
            return "High Risk"

    df["fraud_risk_level"] = df["fraud_risk_score"].apply(risk_category)

    # ===============================
    # Display Results
    # ===============================
    st.write("### 📊 Prediction Results")
    st.caption(f"Optimized decision threshold = **{THRESHOLD:.3f}**")

    st.dataframe(
        df.sort_values("fraud_risk_score", ascending=False),
        use_container_width=True
    )

    # ===============================
    # Summary Metrics
    # ===============================
    st.subheader("📈 Risk Distribution Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "High Risk Claims",
            (df["fraud_risk_level"] == "High Risk").sum()
        )

    with col2:
        st.metric(
            "Medium Risk Claims",
            (df["fraud_risk_level"] == "Medium Risk").sum()
        )

    with col3:
        st.metric(
            "Low Risk Claims",
            (df["fraud_risk_level"] == "Low Risk").sum()
        )

    # ===============================
    # Business Interpretation
    # ===============================
    st.subheader("💼 Business Interpretation")

    st.markdown(
        """
- **High Risk** claims should be **prioritized for manual investigation**.
- **Medium Risk** claims can be reviewed using **additional business rules**.
- **Low Risk** claims can be **fast-tracked** to improve operational efficiency.

This approach balances fraud detection performance and investigation workload.
"""
    )

else:
    st.info("Please upload a CSV file to start fraud risk prediction.")