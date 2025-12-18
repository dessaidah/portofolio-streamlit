import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title="Projects | Churn",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Customer Churn Prediction")
st.write("""
This project demonstrates an **end-to-end machine learning workflow**:
data upload → preprocessing → model training → evaluation → single prediction.
""")

st.divider()

# ------------------------------------------------
# Upload data
# ------------------------------------------------
st.subheader("1️⃣ Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload Customer Churn CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("⬅️ Upload a CSV file to start (e.g. Kaggle Telco Customer Churn dataset).")
    st.stop()

df = pd.read_csv(uploaded_file)

st.success("Dataset loaded successfully!")

st.write("Preview:")
st.dataframe(df.head(10), use_container_width=True)

# ------------------------------------------------
# Target selection
# ------------------------------------------------
st.subheader("2️⃣ Select Target Variable")

target_col = st.selectbox(
    "Choose the churn column (binary)",
    options=df.columns
)

# ------------------------------------------------
# Basic cleaning (Telco-specific)
# ------------------------------------------------
df = df.copy()

if "TotalCharges" in df.columns:
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

df = df.dropna(subset=[target_col])

# Target → binary 0/1
y_raw = df[target_col].astype(str).str.lower().str.strip()

if set(y_raw.unique()) <= {"yes", "no"}:
    y = (y_raw == "yes").astype(int)
else:
    y_num = pd.to_numeric(df[target_col], errors="coerce")
    if len(set(y_num.unique())) != 2:
        st.error("Target column must be binary (Yes/No or 0/1).")
        st.stop()
    vals = sorted(list(set(y_num.unique())))
    y = (y_num == vals[1]).astype(int)

X = df.drop(columns=[target_col])

# Drop ID columns
for col in ["customerID", "CustomerID", "ID", "id", "customer_id"]:
    if col in X.columns:
        X = X.drop(columns=[col])

# ------------------------------------------------
# Feature detection
# ------------------------------------------------
numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = [
    c for c in X.columns if c not in numeric_features
]

# Fill missing values
for c in numeric_features:
    X[c] = X[c].fillna(X[c].median())

for c in categorical_features:
    X[c] = X[c].fillna("Unknown")

st.subheader("3️⃣ Feature Overview")

c1, c2 = st.columns(2)
with c1:
    st.write("**Numeric Features**")
    st.write(numeric_features)

with c2:
    st.write("**Categorical Features**")
    st.write(categorical_features)

# ------------------------------------------------
# Model training
# ------------------------------------------------
st.subheader("4️⃣ Train Model")

test_size = st.slider("Test size", 0.1, 0.4, 0.2, 0.05)
random_state = st.number_input("Random state", 0, 9999, 42)

train_button = st.button("🚀 Train Logistic Regression Model", type="primary")

if train_button:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=int(random_state),
        stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = LogisticRegression(max_iter=2000)

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    st.success("✅ Model training completed")

    m1, m2, m3 = st.columns(3)
    m1.metric("Accuracy", f"{accuracy_score(y_test, y_pred):.3f}")
    m2.metric("F1-Score", f"{f1_score(y_test, y_pred):.3f}")
    m3.metric("ROC-AUC", f"{roc_auc_score(y_test, y_proba):.3f}")

    # Save to session
    st.session_state["pipeline"] = pipeline
    st.session_state["X_columns"] = X.columns.tolist()
    st.session_state["X_ref"] = X
    st.session_state["num_feats"] = numeric_features
    st.session_state["cat_feats"] = categorical_features

st.divider()

# ------------------------------------------------
# Single prediction
# ------------------------------------------------
st.subheader("5️⃣ Predict Churn for a New Customer")

if "pipeline" not in st.session_state:
    st.info("Train the model first to enable prediction.")
    st.stop()

pipeline = st.session_state["pipeline"]
X_cols = st.session_state["X_columns"]
X_ref = st.session_state["X_ref"]
num_feats = st.session_state["num_feats"]
cat_feats = st.session_state["cat_feats"]

with st.form("prediction_form"):
    inputs = {}

    for col in X_cols:
        if col in num_feats:
            default_val = float(X_ref[col].median())
            inputs[col] = st.number_input(col, value=default_val)
        else:
            options = sorted(list(X_ref[col].astype(str).unique()))
            inputs[col] = st.selectbox(col, options)

    submit = st.form_submit_button("🔮 Predict Churn")

if submit:
    input_df = pd.DataFrame([inputs])
    prob = pipeline.predict_proba(input_df)[:, 1][0]
    pred = int(prob >= 0.5)

    st.write(f"**Churn Probability:** `{prob:.3f}`")
    st.write(
        "**Prediction:** "
        + ("❌ Likely to Churn" if pred == 1 else "✅ Likely to Stay")
    )