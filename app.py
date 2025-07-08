import streamlit as st
import qrcode
from PIL import Image
import pandas as pd
from datetime import date, datetime
import os

# 📂 CSV file setup
csv_file = "attendance.csv"
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(csv_file, index=False)

# 🔁 Generate QR code based on today's date
def generate_qr():
    today_str = str(date.today())
    qr = qrcode.make(today_str)
    return qr, today_str

# 🎛 Admin Panel (QR generator)
st.sidebar.title("Admin Panel")
if st.sidebar.button("Generate Today's QR"):
    qr_img, qr_data = generate_qr()
    st.sidebar.image(qr_img, caption="Scan to mark attendance")
    st.sidebar.success(f"QR for: {qr_data}")

# 👨‍🎓 Student Panel
st.title("📸 QR Based Attendance System")
st.markdown("### 🔽 Enter Token from QR and your Name")

token = st.text_input("Enter Token from QR")
name = st.text_input("Enter Your Name")

if st.button("Mark Attendance"):
    today_str = str(date.today())

    if token == today_str:
        current_time = datetime.now().strftime("%H:%M:%S")
        df = pd.read_csv(csv_file)

        # ✅ Prevent duplicate entry
        if ((df['Name'] == name) & (df['Date'] == today_str)).any():
            st.warning("⚠️ Attendance already marked!")
        else:
            new_entry = pd.DataFrame([[name, today_str, current_time]], columns=["Name", "Date", "Time"])
            new_entry.to_csv(csv_file, mode='a', header=False, index=False)
            st.success("✅ Attendance Marked Successfully!")
    else:
        st.error("❌ Invalid Token! Please scan the correct QR.")

# 📊 Optional: Show Attendance Table
if st.checkbox("📋 Show Attendance Record"):
    df = pd.read_csv(csv_file)
    st.dataframe(df)
