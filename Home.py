import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Dessy Saidah | Data Science Portfolio",
    page_icon="✨",
    layout="wide"
)

header_image = Image.open("assets/header.png")
st.image(header_image, use_container_width=True)

st.title("Dessy Saidah | Data Science Portfolio ✨")
st.write(
    "I build **data-driven insights** and **machine learning applications** "
    "that support better business decisions — delivered through interactive Streamlit apps."
)

cta1, cta2, cta3 = st.columns([1, 1, 2])

with cta1:
    st.page_link("pages/2_Projects.py", label="📉 View Projects", use_container_width=True)

with cta2:
    st.page_link("pages/3_Contact Me.py", label="📫 Contact Me", use_container_width=True)

with cta3:
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


st.subheader("Featured Project")

p_left, p_right = st.columns([2, 1])

with p_left:
    st.markdown("### 📉 Customer Churn Prediction")
    st.write(
        "An end-to-end machine learning application that allows users to "
        "upload a dataset, train a model, evaluate performance, and predict "
        "customer churn probability."
    )

    st.markdown("""
**Key features:**
- Upload CSV dataset  
- Automatic preprocessing  
- Train & evaluate ML model  
- Predict churn probability  
""")

    st.page_link(
        "pages/2_Projects.py",
        label="➡️ Open Project",
        use_container_width=True
    )

with p_right:
    st.info("Tip: Visit **Projects** to interact with the full ML application.")

st.divider()

st.caption("Thank you for visiting — explore the pages from the sidebar.")