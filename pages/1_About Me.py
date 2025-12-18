import streamlit as st

st.set_page_config(
    page_title="About Me",
    page_icon="👩🏻",
    layout="wide"
)

st.title("Hi, I'm Dessy 👋")
st.markdown("### Data Analyst & Machine Learning Enthusiast")

st.write(
    "I transform data into **actionable insights** and build "
    "**machine learning models** that support better business decisions."
)

st.divider()

# ---- About Me ----
st.subheader("About Me")
st.write("""
I am passionate about turning raw, messy data into clear insights.
My main interest lies in **machine learning**, **business analytics**, 
and deploying models into **interactive applications** using Streamlit.

I enjoy working on end-to-end projects, from data preparation and modeling 
to explaining results in a way that stakeholders can easily understand.
""")

# ---- What I Do ----
st.subheader("What I Do")

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    📊 **Data Analysis & Visualization**  
    Explore data, find patterns, and communicate insights clearly.
    """)

    st.markdown("""
    🤖 **Machine Learning Modeling**  
    Build and evaluate predictive models for real-world problems.
    """)

with c2:
    st.markdown("""
    🧠 **Business Insight & Storytelling**  
    Translate model outputs into meaningful business recommendations.
    """)

    st.markdown("""
    🚀 **Model Deployment with Streamlit**  
    Turn models into interactive web applications.
    """)

# ---- Skills ----
st.subheader("Skills")

skills = [
    "Python", "SQL", "Power BI", "Machine Learning",
    "Microsoft Office", "Streamlit"
]

st.write(" ".join([f"`{skill}`" for skill in skills]))

st.divider()

st.info("👉 Check out the **Projects** page to see my machine learning work in action.")