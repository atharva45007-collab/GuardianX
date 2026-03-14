import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="GuardianX Security Dashboard",
    page_icon="🛡",
    layout="wide"
)

# ---------- Custom Theme ----------
st.markdown("""
<style>
body {
    background-color: #0b1f3a;
}

h1, h2, h3 {
    color: #00ff9c;
}

.sidebar .sidebar-content {
    background-color: #06152b;
}

.stButton>button {
    background-color: #00ff9c;
    color: black;
    font-weight: bold;
}

.alert-high {
    color: red;
    font-weight: bold;
}

.alert-medium {
    color: orange;
    font-weight: bold;
}

.alert-safe {
    color: green;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("🛡 GuardianX")
st.caption("Your Shield Against Ransomware & Data Leaks")

# ---------- Sidebar Navigation ----------
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🦠 Ransomware Detection", "🔎 Data Leak Check", "📊 Reports"]
)

# ---------- HOME DASHBOARD ----------
if menu == "🏠 Home":

    st.header("Security Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Threats Scanned Today", "1,245")
    col2.metric("Ransomware Detected", "2")
    col3.metric("Data Leaks Found", "1")

    st.subheader("System Status")

    st.success("✔ System Monitoring Active")

    st.subheader("Live Security Logs")

    logs = [
        "Scanning file system...",
        "Checking network traffic...",
        "Analyzing suspicious activity...",
        "Monitoring encryption patterns..."
    ]

    for log in logs:
        st.text(log)
        time.sleep(0.3)

# ---------- RANSOMWARE DETECTION ----------
elif menu == "🦠 Ransomware Detection":

    st.header("Ransomware Detection System")

    st.write("Scan your system to detect suspicious encryption activity.")

    if st.button("Start Scan"):

        with st.spinner("Scanning files..."):
            time.sleep(2)

        st.error("⚠️ Ransomware Activity Detected!")

        st.write("Suspicious file encryption behavior identified.")

# ---------- DATA LEAK CHECK ----------
elif menu == "🔎 Data Leak Check":

    st.header("Data Leak Scanner")

    st.write("Check if sensitive files are exposed.")

    data = {
        "File Name": ["customer_data.csv", "passwords.txt", "finance_report.pdf"],
        "Risk Level": ["🔴 High", "🟡 Medium", "🟢 Safe"]
    }

    df = pd.DataFrame(data)

    st.table(df)

# ---------- REPORTS ----------
elif menu == "📊 Reports":

    st.header("Security Reports")

    st.write("Generate system security reports.")

    if st.button("Generate Report"):

        st.success("Report Generated Successfully")

        report_text = """
GuardianX Security Report

Threats Scanned: 1245
Ransomware Detected: 2
Data Leak Alerts: 1
System Status: Secure
"""

        st.download_button(
            label="Download Report",
            data=report_text,
            file_name="guardianx_report.txt"
        )
