import streamlit as st
from datetime import date, datetime
import pandas as pd
import qrcode
from PIL import Image
import io
import os
from streamlit_js_eval import streamlit_js_eval

# Dummy user database
users = {
    "teacher1": {"password": "teach123", "role": "teacher"},
    "student1": {"password": "stud123", "role": "student"},
    "student2": {"password": "stud456", "role": "student"},
}

# CSV Setup
csv_file = "attendance.csv"
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(csv_file, index=False)

# QR Code Generator
def generate_qr():
    today_str = str(date.today())
    streamlit_url = "https://aryanrout-qr-attendance.streamlit.app"
    link = f"{streamlit_url}/?token={today_str}"
    qr = qrcode.make(link)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf, today_str, link

# UI
st.set_page_config(page_title="QR Attendance", page_icon="📚")
st.title("📚 QR Attendance System with QR Scan")

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Login
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

# Teacher View
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

# Student View with QR Scanner
elif st.session_state.role == "student":
    st.sidebar.title("👨‍🎓 Student Panel")
    st.sidebar.success(f"Logged in as: {st.session_state.username}")

    st.subheader("📷 Scan QR Code Below")

    scanned = streamlit_js_eval(js_expressions="await new Promise(resolve => {"
                                               "const video = document.createElement('video');"
                                               "video.setAttribute('autoplay', '');"
                                               "video.setAttribute('playsinline', '');"
                                               "video.style.display = 'none';"
                                               "document.body.appendChild(video);"
                                               "navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}})"
                                               ".then(stream => {"
                                               "video.srcObject = stream;"
                                               "const canvas = document.createElement('canvas');"
                                               "const context = canvas.getContext('2d');"
                                               "const interval = setInterval(() => {"
                                               "canvas.width = video.videoWidth;"
                                               "canvas.height = video.videoHeight;"
                                               "context.drawImage(video, 0, 0, canvas.width, canvas.height);"
                                               "try {"
                                               "const code = jsQR(context.getImageData(0, 0, canvas.width, canvas.height).data, canvas.width, canvas.height);"
                                               "if (code) {"
                                               "clearInterval(interval);"
                                               "video.srcObject.getTracks().forEach(track => track.stop());"
                                               "resolve(code.data);"
                                               "}"
                                               "} catch(e) {}"
                                               "}, 500);"
                                               "});"
                                               "});",
                                  key="qrscan")

    if scanned:
        st.success(f"✅ Token Scanned from QR: {scanned}")
        token = scanned.split("token=")[-1]
    else:
        token = ""

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
