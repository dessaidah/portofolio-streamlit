import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="Food Delivery Time Prediction",
    page_icon="🍔",
    layout="wide"
)

@st.cache_resource
def load_artifacts():
    from xgboost import XGBRegressor 
    
    model = joblib.load("projects/models/xgb_model.pkl")
    scaler = joblib.load("projects/models/scaler.pkl")
    ohe_columns = joblib.load("projects/models/ohe_columns.pkl")
    return model, scaler, ohe_columns

model, scaler, ohe_columns = load_artifacts()

st.header("🍔 Delivery Time Prediction")
st.write("Estimate food delivery time based on order conditions")

# ======================
# USER INPUT
# ======================
distance = st.number_input("Distance (km)", min_value=0.1, max_value=50.0, value=5.0)
order_hour = st.slider("Order Hour", 0, 23, 12)
multiple_deliveries = st.selectbox("Multiple Deliveries", [0, 1, 2, 3])

traffic = st.selectbox(
    "Traffic Density",
    ["Low", "Medium", "High", "Jam"]
)

weather = st.selectbox(
    "Weather Conditions",
    ["Sunny", "Cloudy", "Fog", "Stormy", "Windy", "Sandstorms"]
)

festival = st.selectbox("Festival", ["No", "Yes"])
city = st.selectbox("City", ["Urban", "Semi-Urban", "Metropolitan"])

age = st.slider("Driver Age", 18, 60, 30)
rating = st.slider("Driver Rating", 1.0, 5.0, 4.5)
vehicle_condition = st.slider("Vehicle Condition", 0, 2, 1)

# ======================
# BUILD INPUT DATAFRAME
# ======================
input_df = pd.DataFrame([{
    "Distance_km": distance,
    "Order_Hour": order_hour,
    "multiple_deliveries": multiple_deliveries,
    "Delivery_person_Age": age,
    "Delivery_person_Ratings": rating,
    "Vehicle_condition": vehicle_condition,
    "Road_traffic_density": traffic,
    "Weather_conditions": weather,
    "Festival": festival,
    "City": city
}])

# ======================
# PREPROCESSING
# ======================
# Scale numerical
num_cols = joblib.load("projects/models/num_cols.pkl")

input_df[num_cols] = scaler.transform(input_df[num_cols])

final_features = joblib.load("projects/models/final_feature_columns.pkl")

# One-hot encode categorical
input_encoded = pd.get_dummies(input_df, drop_first=True)

# Align with training columns
input_final = input_encoded.reindex(
    columns=final_features,
    fill_value=0
)

# ======================
# PREDICTION
# ======================
if st.button("Predict Delivery Time"):
    prediction = model.predict(input_final)[0]
    st.success(f"Estimated Delivery Time: {prediction:.1f} minutes")
