import streamlit as st
import pandas as pd
import qrcode
from datetime import datetime, date
from PIL import Image
import io
import os

from streamlit_js_eval import streamlit_js_eval  # ✅ for mobile QR scan

# CSV Setup
csv_file = "attendance.csv"
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(csv_file, index=False)

# QR Code Generator
def generate_qr():
    today_str = str(date.today())
    qr = qrcode.make(today_str)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf, today_str

st.set_page_config(page_title="QR Attendance", page_icon="📚")

# Role selection
role = st.sidebar.selectbox("Select Role", ["Student", "Teacher"])

# =========================== TEACHER ===========================
if role == "Teacher":
    st.sidebar.title("Admin Panel")
    if st.sidebar.button("Generate Today's QR"):
        qr_img, qr_data = generate_qr()
        st.sidebar.image(qr_img, caption=f"QR for: {qr_data}")
        st.sidebar.success("✅ QR Generated")

# =========================== STUDENT ===========================
else:
    st.title("📚 QR Attendance System with QR Scan")
    st.subheader("📸 Scan QR Code Below")

    # 👇 Open Camera to Scan Token
    qr_code = streamlit_js_eval(
        js_expressions="await (async () => { const txt = await navigator.clipboard.readText(); return txt; })();",
        key="qrscanner",
        debounce=3
    )

    st.write("Scanned Token: ", qr_code or "Waiting...")

    name = st.text_input("Enter Your Name")

    if st.button("✅ Mark Attendance"):
        today_str = str(date.today())

        if qr_code == today_str:
            df = pd.read_csv(csv_file)
            if ((df['Name'] == name) & (df['Date'] == today_str)).any():
                st.warning("⚠️ Attendance Already Marked")
            else:
                now = datetime.now().strftime("%H:%M:%S")
                new_entry = pd.DataFrame([[name, today_str, now]], columns=["Name", "Date", "Time"])
                new_entry.to_csv(csv_file, mode='a', header=False, index=False)
                st.success("✅ Attendance Marked")
        else:
            st.error("❌ Invalid QR Token")

    # ✅ Optional: Show full record
    if st.checkbox("📋 Show Attendance Record"):
        df = pd.read_csv(csv_file)
        st.dataframe(df)
