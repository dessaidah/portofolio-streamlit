import streamlit as st

st.set_page_config(page_title="Contact Me", page_icon="📫", layout="wide")

st.title("📫 Contact Me")
st.write("Feel free to reach out for collaboration, opportunities, or questions about my projects.")

st.divider()


EMAIL = "dessynasution2000@email.com"
LINKEDIN = "https://linkedin.com/in/dessysaidah"
GITHUB = "https://github.com/dessaidah"
CV_URL = "https://drive.google.com/file/d/1mMuiMC8VnRJGX0ri0vLmyrnaRU5FIiMu/view?usp=sharing" 

# -------------------------
# Contact Cards
# -------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("✉️ Email")
    st.write('Got any questions?')
    st.markdown(f"[Send me an email](mailto:{EMAIL})")

with c2:
    st.subheader("💼 LinkedIn")
    st.write("Connect with me")
    st.markdown(f"[Open LinkedIn profile]({LINKEDIN})")

with c3:
    st.subheader("💻 GitHub")
    st.write("See my other projects")
    st.markdown(f"[Open GitHub profile]({GITHUB})")

if CV_URL:
    st.markdown(f"📄 **CV/Resume:** [Download here]({CV_URL})")

st.divider()

# -------------------------
# Contact Form (demo)
# -------------------------
st.subheader("Send a message (demo form)")

st.info(
    "This form collects inputs but does not automatically send emails yet. "
)

with st.form("contact_form"):
    name = st.text_input("Your name")
    from_email = st.text_input("Your email")
    topic = st.selectbox("Topic", ["Collaboration", "Job Opportunity", "Project Question", "Other"])
    message = st.text_area("Message", height=150)
    submitted = st.form_submit_button("📩 Submit")

if submitted:
    if not name or not from_email or not message:
        st.error("Please fill in your name, email, and message.")
    else:
        st.success("Thanks! Your message has been captured ✅")
        st.write("**Preview:**")
        st.write(f"- Name: {name}")
        st.write(f"- Email: {from_email}")
        st.write(f"- Topic: {topic}")
        st.write(f"- Message: {message}")

st.divider()
st.caption("Tip: You can also reach me faster via email or LinkedIn above.")