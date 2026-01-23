import streamlit as st
st.title("📁 Projects")

project = st.selectbox(
    "Select a project",
    (
        "Customer Churn Prediction",
        "Insurance Fraud Risk Prediction"
    )
)

if project == "Customer Churn Prediction":
    st.switch_page("projects/churn_app.py")

elif project == "Insurance Fraud Risk Prediction":
    st.switch_page("projects/fraud_app.py")