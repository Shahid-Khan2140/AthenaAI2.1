import streamlit as st
import google.generativeai as genai
import os
import base64
import pkg_resources
from dotenv import load_dotenv

# =========================
# 🔑 Load .env API key
# =========================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# --- Check for API key early ---
if not API_KEY:
    st.error("❌ No API key found. Please create a `.env` file with GEMINI_API_KEY=AIxxxx from https://aistudio.google.com/app/apikey.")
    st.stop()

# --- Check SDK version ---
try:
    version = pkg_resources.get_distribution("google-generativeai").version
    if tuple(map(int, version.split("."))) < (0, 6, 0):
        st.error("⚠️ Please upgrade google-generativeai to version 0.6.0 or higher for Gemini 2.5 Flash support.")
        st.stop()
except Exception:
    pass

# =========================
# 🖥️ Streamlit Page Setup
# =========================
st.set_page_config(page_title="Athena AI Career Advisor", page_icon="logo.png", layout="wide")

# --- Convert image to base64 ---
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        return ""

st.markdown("""
<style>
/* 🔷 Header bar */
.header {
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
    padding: 20px 40px; border-radius: 16px;
    color: #f1f1f1; margin-bottom: 30px;
}
.header h1 { margin: 0; font-size: 2.2rem; color: #fff; }
.logo-img {
    border-radius: 50%; height: 60px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    margin-right: 15px;
}

/* 🔹 Card form container */
.card {
    background-color: transparent;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 25px; border-radius: 14px;
    box-shadow: 0 0 15px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}

/* 🔹 AI Response Box — Dark Mode Harmony */
.response-box {
    background: rgba(32, 35, 42, 0.9);
    color: #e9e9e9;
    padding: 25px;
    border-left: 5px solid #1e90ff;
    border-radius: 10px;
    margin-top: 20px;
    font-size: 1rem;
    line-height: 1.6;
    white-space: pre-wrap;
    box-shadow: 0 0 12px rgba(0,0,0,0.3);
}

/* 🔹 Light Mode Adjustment */
@media (prefers-color-scheme: light) {
    .response-box {
        background: #ffffff;
        color: #212121;
        border-left: 5px solid #1c6dd0;
    }
    .card {
        background-color: #ffffff;
        color: #111111;
        box-shadow: 0 0 8px rgba(0,0,0,0.1);
    }
}

/* 🔹 Logout button styling */
div[data-testid="stButton"] button {
    background-color: #ff4b4b;
    color: white;
    padding: 10px 25px;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    margin-top: 20px;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] button:hover {
    background-color: #ff3333;
}
body, .stApp {
        background-color: #0e1117 !important;
        color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 Login System
# =========================
def login():
    st.title("Athena AI 2.1 Login")
    st.write("Please enter your credentials to continue.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username == "Shahid Khan" and password == "sk2140":
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

# =========================
# 🧭 Header Section
# =========================
def header():
    logo_b64 = get_image_base64("logo.png")
    col1, col2 = st.columns([8, 1])

    with col1:
        st.markdown(f"""
        <div class="header">
            <div style="display:flex; align-items:center;">
                <img src="data:image/png;base64,{logo_b64}" class="logo-img" />
                <div style="margin-left:20px;">
                    <h1>Athena AI – Career Advisor for CS Students</h1>
                    <p style="margin:0;">Powered by Gemini • Built by Shahid Khan</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("Logout", key="logout", type="primary"):
            st.session_state.logged_in = False
            st.rerun()

# =========================
# 🧠 Career Quiz
# =========================
def career_quiz():
    with st.form("career_quiz"):
        st.markdown('<div class="card">', unsafe_allow_html=True)

        q1 = st.radio("1️⃣ What do you enjoy most?", [
            "Solving logic problems", "Designing websites", "Automating tasks", "Protecting systems", "Analyzing data"
        ])
        q2 = st.radio("2️⃣ Which tools/languages do you prefer?", [
            "Python", "HTML/CSS/JS", "Linux/Shell", "SQL/Excel", "Java/C++"
        ])
        q3 = st.radio("3️⃣ What kind of projects excite you?", [
            "AI/ML", "Web design", "Ethical hacking", "Cloud & DevOps", "Dashboards & data tools"
        ])
        q4 = st.radio("4️⃣ What's your ideal work style?", [
            "Research & build models", "Create beautiful apps", "Secure systems",
            "Manage infrastructure", "Visualize trends"
        ])

        submit = st.form_submit_button("🔍 Get Career Advice")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        st.markdown("### ✅ Athena’s Personalized Career Recommendation")
        with st.spinner("Analyzing your preferences..."):
            prompt = f"""
            You are Athena AI 2.5 Flash — a professional career advisor for Computer Science students.

            Analyze the following student interests and suggest the most suitable career path:
            - Enjoyment: {q1}
            - Preferred tools: {q2}
            - Favorite projects: {q3}
            - Work style: {q4}

            Please respond with:
            - Recommended career field (AI/ML, Web Dev, Cybersecurity, DevOps, Data Science)
            - Step-by-step roadmap (languages, tools, frameworks)
            - Top job roles and skills needed
            - Certifications or internships to pursue
            - Motivational closing note in a friendly tone.
            """

            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel("gemini-2.5-flash")
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                st.markdown(f'<div class="response-box">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.info("👉 Ensure your API key comes from https://aistudio.google.com/app/apikey and google-generativeai ≥ 0.6.0 is installed.")

# =========================
# 🚀 Main Execution
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    header()
    career_quiz()
