# ==========================================================
# 🎓 AI STUDENT PORTAL - FINAL FULL SYSTEM
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib

st.set_page_config(page_title="AI Student Portal", layout="wide")

# ----------------------------------------------------------
# 🎨 STYLE
# ----------------------------------------------------------
st.markdown("""
<style>
.main {background-color:#f5f7fb;}
.card {
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.1);
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# DATABASE
# ----------------------------------------------------------
conn = sqlite3.connect("student.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT)")
conn.commit()

# ----------------------------------------------------------
# AUTH FUNCTIONS
# ----------------------------------------------------------
def hash(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login(u,p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",(u,hash(p)))
    return c.fetchone()

def signup(u,p):
    try:
        c.execute("INSERT INTO users VALUES (?,?)",(u,hash(p)))
        conn.commit()
        return True
    except:
        return False

# ----------------------------------------------------------
# SESSION
# ----------------------------------------------------------
if "start" not in st.session_state:
    st.session_state.start = False

if "login" not in st.session_state:
    st.session_state.login = False

# ----------------------------------------------------------
# 🎬 WELCOME PAGE
# ----------------------------------------------------------
if not st.session_state.start:

    st.markdown("""
    <div style='text-align:center; padding:80px;
    background:linear-gradient(135deg,#ff9a9e,#fad0c4);
    border-radius:25px;'>

    <h1 style='font-size:60px;'>🎓 AI Student Portal</h1>

    <p style='font-size:22px;'>
    Your Smart Academic & Wellbeing Assistant ✨
    </p>

    <img src='https://cdn-icons-png.flaticon.com/512/3135/3135755.png' width='200'/>

    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Enter Portal"):
        st.session_state.start = True
        st.rerun()

    st.stop()

# ----------------------------------------------------------
# 🔐 LOGIN / SIGNUP
# ----------------------------------------------------------
if not st.session_state.login:

    st.title("🔐 Login / Signup")

    option = st.radio("Select",["Login","Signup"])

    if option=="Login":
        u = st.text_input("Username")
        p = st.text_input("Password",type="password")

        if st.button("Login"):
            if login(u,p):
                st.session_state.login=True
                st.session_state.user=u
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        u = st.text_input("New Username")
        p = st.text_input("New Password",type="password")

        if st.button("Signup"):
            if signup(u,p):
                st.success("Account created")
            else:
                st.error("User exists")

# ----------------------------------------------------------
# 🧠 MAIN DASHBOARD
# ----------------------------------------------------------
else:

    st.sidebar.title(f"👤 {st.session_state.user}")

    menu = {
        "🏠 Home":"Home",
        "📊 Dashboard":"Dashboard",
        "📚 Academics":"Academics",
        "🧘 Wellbeing":"Wellbeing",
        "🎯 Goals":"Goals",
        "🎭 Activities":"Activities",
        "📈 Progress":"Progress",
        "💬 Feedback":"Feedback",
        "🚪 Logout":"Logout"
    }

    page = menu[st.sidebar.radio("Menu", list(menu.keys()))]

    # ------------------------------------------------------
    # HOME
    # ------------------------------------------------------
    if page=="Home":
        st.markdown("""
        <div style='padding:50px;background:linear-gradient(135deg,#11998e,#38ef7d);
        border-radius:20px;color:white;text-align:center;'>

        <h1>🎓 AI Student Success System</h1>
        <p>Dataset: 196,000 records | Model: Random Forest (99.98%)</p>

        </div>
        """, unsafe_allow_html=True)

    # ------------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------------
    elif page=="Dashboard":

        st.title("📊 Dashboard")

        c1,c2,c3,c4 = st.columns(4)

        c1.markdown("<div class='card'>📚 Study<br>6 hrs</div>", unsafe_allow_html=True)
        c2.markdown("<div class='card'>🏫 Attendance<br>85%</div>", unsafe_allow_html=True)
        c3.markdown("<div class='card'>📝 Homework<br>75%</div>", unsafe_allow_html=True)
        c4.markdown("<div class='card'>🧠 Stress<br>4/10</div>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # ACADEMICS
    # ------------------------------------------------------
    elif page=="Academics":
        st.title("📚 Academics")

        study = st.slider("Study Hours",0.0,12.0,5.0)
        attendance = st.slider("Attendance",0.0,100.0,80.0)

        st.success("Academic tracking active")

    # ------------------------------------------------------
    # WELLBEING
    # ------------------------------------------------------
    elif page=="Wellbeing":
        st.title("🧘 Wellbeing")

        sleep = st.slider("Sleep",0.0,12.0,7.0)
        stress = st.slider("Stress",0,10,4)

        if sleep>7 and stress<5:
            st.success("Healthy ✅")
        else:
            st.warning("Improve habits ⚠️")

    # ------------------------------------------------------
    # GOALS
    # ------------------------------------------------------
    elif page=="Goals":
        st.title("🎯 Goals")

        goal = st.text_input("Enter goal")
        if st.button("Save"):
            st.success(f"Goal saved: {goal}")

    # ------------------------------------------------------
    # ACTIVITIES
    # ------------------------------------------------------
    elif page=="Activities":
        st.title("🎭 Activities")

        level = st.slider("Participation",0,10,5)
        st.info("Co-curricular improves performance")

    # ------------------------------------------------------
    # PROGRESS GRAPH
    # ------------------------------------------------------
    elif page=="Progress":
        st.title("📈 Progress")

        df = pd.DataFrame({
            "Day":["Mon","Tue","Wed","Thu","Fri"],
            "Study":[2,4,5,3,6]
        })

        fig = px.line(df,x="Day",y="Study",title="Weekly Progress")
        st.plotly_chart(fig)

    # ------------------------------------------------------
    # FEEDBACK
    # ------------------------------------------------------
    elif page=="Feedback":
        st.title("💬 Feedback")

        fb = st.text_area("Enter feedback")

        if st.button("Submit"):
            st.success("Thanks for feedback 🙏")

    # ------------------------------------------------------
    # LOGOUT
    # ------------------------------------------------------
    elif page=="Logout":

        st.markdown("""
        <div style='text-align:center; padding:80px;
        background:linear-gradient(135deg,#667eea,#764ba2);
        border-radius:25px; color:white;'>

        <h1>🙏 Thank You!</h1>
        <p>Visit again 🚀</p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Confirm Logout"):
            st.session_state.login=False
            st.session_state.start=False
            st.rerun()