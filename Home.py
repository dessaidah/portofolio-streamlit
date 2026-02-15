import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Dessy Saidah | Data Science Portfolio",
    page_icon="✨",
    layout="wide"
)

header_image = Image.open("assets/header.png")
st.image(header_image, width=900)

st.title("Dessy Saidah | Data Science Portfolio ✨")
st.write(
    "I build **data-driven insights** and **machine learning applications** "
    "that support better business decisions — delivered through interactive Streamlit apps."
)

cta1, cta2 = st.columns([1, 2])

with cta1:
    st.page_link("pages/6_Contact Me.py", label="📫 Contact Me", use_container_width=True)

with cta2:
    st.markdown(
        "🔗 **Links:** "
        "[GitHub](https://github.com/dessaidah) · "
        "[LinkedIn](https://linkedin.com/in/dessysaidah)"
    )

st.divider()


st.subheader("About Me")

left, right = st.columns([2, 1])

with left:
    st.write(
        "I am a data enthusiast with a strong interest in **machine learning** "
        "and **business analytics**. I enjoy transforming raw data into meaningful "
        "insights and deploying predictive models into interactive applications."
    )

    st.markdown("""
**What I do:**
- 📊 Data Analysis & Visualization  
- 🤖 Machine Learning Modeling  
- 🧠 Business Insight & Storytelling  
- 🚀 Model Deployment with Streamlit  
""")

    st.page_link(
        "pages/1_About Me.py",
        label="👤 Read full About Me",
        use_container_width=True
    )

with right:
    st.markdown("**Core Skills**")
    skills = [
        "Python", "Pandas", "NumPy",
        "Scikit-Learn", "SQL", "Streamlit"
    ]
    st.write(" ".join([f"`{s}`" for s in skills]))

st.divider()


st.subheader("🚀 Featured Projects")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📉 Customer Churn Prediction")
    st.write(
        "End-to-end ML app for predicting customer churn probability "
        "with model evaluation and explainability."
    )
    if st.button("Open Churn Project"):
        st.switch_page("pages/2_Churn Prediction.py")

with col2:
    st.markdown("### 🚗 Insurance Fraud Risk Prediction")
    st.write(
        "Fraud risk scoring system using CatBoost with optimized threshold "
        "to support claim screening and investigation prioritization."
    )
    if st.button("Open Fraud Project"):
        st.switch_page("pages/3_Fraud Risk Prediction.py")

with col3:
    st.markdown("### 🍔 Food Delivery Time Prediction")
    st.write(
        "Explainable machine learning model to predict food delivery time "
        "based on distance, traffic, and operational factors."
    )
    if st.button("Open Delivery Time Project"):
        st.switch_page("pages/4_Delivery Time Prediction.py")

st.divider()

st.caption("Thank you for visiting — explore the pages from the sidebar.")
