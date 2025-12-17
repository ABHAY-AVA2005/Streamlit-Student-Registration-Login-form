import streamlit as st
import sqlite3

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Student Portal", page_icon="🎓")

# ------------------ DATABASE CONNECTION ------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# ------------------ FUNCTIONS ------------------
def register_student(username, email, password):
    try:
        cursor.execute(
            "INSERT INTO students (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_student(username, password):
    cursor.execute(
        "SELECT * FROM students WHERE username=? AND password=?",
        (username, password)
    )
    return cursor.fetchone()

# ------------------ UI ------------------
st.title("🎓 Student Registration & Login System")

tab1, tab2 = st.tabs(["📝 Register", "🔐 Login"])

# ================= REGISTER =================
with tab1:
    st.subheader("Create Account")

    with st.form("register_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            reg_username = st.text_input("👤 Username")
        with col2:
            reg_email = st.text_input("📧 Email")

        reg_password = st.text_input("🔑 Password", type="password")

        register_btn = st.form_submit_button("Register")

    if register_btn:
        if reg_username and reg_email and reg_password:
            success = register_student(reg_username, reg_email, reg_password)
            if success:
                st.success("✅ Registration successful! Please login.")
            else:
                st.error("❌ Username or Email already exists")
        else:
            st.warning("⚠️ All fields are required")

# ================= LOGIN =================
with tab2:
    st.subheader("Login")

    with st.form("login_form"):
        login_username = st.text_input("👤 Username", key="login_user")
        login_password = st.text_input("🔑 Password", type="password", key="login_pass")

        login_btn = st.form_submit_button("Login")

    if login_btn:
        if login_username and login_password:
            user = login_student(login_username, login_password)
            if user:
                st.success(f"🎉 Welcome, {login_username}!")
                st.balloons()
            else:
                st.error("❌ Invalid username or password")
        else:
            st.warning("⚠️ Please enter all fields")

# ================= VIEW USERS =================
with st.expander("📋 View Registered Students"):
    users = cursor.execute("SELECT username, email FROM students").fetchall()
    if users:
        for u in users:
            st.write(f"👤 **{u[0]}** | 📧 {u[1]}")
    else:
        st.info("No students registered yet")
