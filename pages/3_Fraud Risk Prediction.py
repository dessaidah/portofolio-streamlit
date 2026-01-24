import streamlit as st
import pandas as pd
import joblib
from catboost import CatBoostClassifier
from pathlib import Path

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Insurance Fraud Risk Prediction",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Insurance Claim Fraud Risk Prediction")
st.markdown("""
This application predicts **fraud risk probability** for insurance claims  
using a **CatBoost model with optimized threshold**.
""")

st.divider()

# ===============================
# Load Artifacts
# ===============================
@st.cache_resource
def load_artifacts():
    model = CatBoostClassifier()
    model.load_model("projects/models/model_cat.cbm")

    feature_cols = joblib.load("projects/models/feature_columns.pkl")
    threshold = joblib.load("projects/models/best_threshold.pkl")

    return model, feature_cols, threshold


model, FEATURE_COLS, BEST_THRESHOLD = load_artifacts()

# ===============================
# Upload Data
# ===============================
st.subheader("📤 Upload Dataset")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Data uploaded successfully!")
    st.write("Preview of uploaded data:")
    st.dataframe(df.head())

    # ===============================
    # CLEANING (WAJIB)
    # ===============================

    # 1. Drop unnamed index column
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # 2. Drop target if exists
    TARGET_COL = "FraudFound_P"
    if TARGET_COL in df.columns:
        df = df.drop(columns=[TARGET_COL])

    # ===============================
    # REORDER COLUMNS (PALING PENTING)
    # ===============================
    missing_cols = set(FEATURE_COLS) - set(df.columns)
    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        st.stop()

    df = df[FEATURE_COLS]

    # ===============================
    # TYPE CASTING
    # ===============================
    NUMERIC_FEATURES = ["Age"]
    CATEGORICAL_FEATURES = [c for c in FEATURE_COLS if c not in NUMERIC_FEATURES]

    # numeric
    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # categorical
    for col in CATEGORICAL_FEATURES:
        df[col] = df[col].astype(str)

    st.subheader("🧪 Feature Processing Summary")
    st.write("Numeric features:", NUMERIC_FEATURES)
    st.write("Categorical features:", CATEGORICAL_FEATURES)

    # ===============================
    # PREDICTION
    # ===============================
    st.subheader("🔍 Fraud Risk Scoring")

    fraud_prob = model.predict_proba(df)[:, 1]
    fraud_pred = (fraud_prob >= BEST_THRESHOLD).astype(int)

    df_result = df.copy()
    df_result["Fraud_Probability"] = fraud_prob
    df_result["Fraud_Prediction"] = fraud_pred

    st.success("Prediction completed!")
    st.write(f"Threshold used: **{BEST_THRESHOLD:.3f}**")
    st.dataframe(df_result.head(10))

    # ===============================
    # Download
    # ===============================
    csv = df_result.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Prediction Result",
        csv,
        "fraud_prediction_result.csv",
        "text/csv"
    )


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "projects" / "models" / "catboost_fraud_model.cbm"
CONFIG_PATH = BASE_DIR / "projects" / "models" / "best_threshold.pkl"
CAT_FEATURES_PATH = BASE_DIR / "projects" / "models" / "feature_columns.pkl"