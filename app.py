import streamlit as st
from datetime import date, datetime
import pandas as pd
import qrcode
from PIL import Image
import io
import os

# -------------------------------
# 🔐 Dummy user database
users = {
    "teacher1": {"password": "teach123", "role": "teacher"},
    "student1": {"password": "stud123", "role": "student"},
    "student2": {"password": "stud456", "role": "student"},
}

# -------------------------------
# 📄 CSV Setup
csv_file = "attendance.csv"
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(csv_file, index=False)

# -------------------------------
# 📷 QR Code Generator (URL-based QR)
def generate_qr():
    today_str = str(date.today())
    # 👇 Replace this with your actual deployed Streamlit URL 👇
    streamlit_url = "https://qr-attendance-yx4bifqxdnhwqp6w4hb9fm.streamlit.app/"
    link = f"{streamlit_url}/?token={today_str}"
    qr = qrcode.make(link)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf, today_str, link

# -------------------------------
# 🧠 Main Logic Starts Here
st.set_page_config(page_title="QR Attendance", page_icon="📚")
st.title("📚 QR Attendance System with Login")

# Session State for Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Login form
if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

# -------------------------------
# 👨‍🏫 Teacher Panel
elif st.session_state.role == "teacher":
    st.sidebar.title("👨‍🏫 Teacher Panel")
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    
    if st.sidebar.button("📸 Generate Today's QR Code"):
        qr_img, qr_token, link = generate_qr()
        st.image(qr_img, caption="📷 Scan to mark attendance")
        st.success(f"✅ QR generated for token: `{qr_token}`")
        st.info(f"🔗 Link inside QR: {link}")

    if st.sidebar.checkbox("📄 Show Attendance Record"):
        df = pd.read_csv(csv_file)
        st.dataframe(df)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# -------------------------------
# 👨‍🎓 Student Panel
elif st.session_state.role == "student":
    st.sidebar.title("👨‍🎓 Student Panel")
    st.sidebar.success(f"Logged in as: {st.session_state.username}")

    # 🧠 Auto-fetch token from URL
    query_params = st.experimental_get_query_params()
    default_token = query_params.get("token", [""])[0]

    st.subheader("📝 Mark Your Attendance")

    token = st.text_input("Token (auto-filled from QR)", value=default_token)
    name = st.text_input("Enter Your Name")

    if st.button("✅ Mark Attendance"):
        today_str = str(date.today())
        if token == today_str:
            current_time = datetime.now().strftime("%H:%M:%S")
            df = pd.read_csv(csv_file)
            if ((df['Name'] == name) & (df['Date'] == today_str)).any():
                st.warning("⚠️ Attendance already marked!")
            else:
                new_entry = pd.DataFrame([[name, today_str, current_time]], columns=["Name", "Date", "Time"])
                new_entry.to_csv(csv_file, mode='a', header=False, index=False)
                st.success("✅ Attendance Marked Successfully!")
        else:
            st.error("❌ Invalid Token!")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
