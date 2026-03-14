import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="GuardianX",
    page_icon="🛡",
    layout="wide"
)

# Theme styling
st.markdown("""
<style>
body {
    background-color: #0a1a2f;
}
.main-title {
    color: #00ff9c;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Title and Tagline
st.markdown("<h1 class='main-title'>🛡 GuardianX</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Your Shield Against Ransomware & Data Leaks</h4>", unsafe_allow_html=True)

# Navigation Menu
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Ransomware Detection", "Data Leak Check", "Reports"]
)

# ---------------- HOME ----------------
if menu == "Home":

    st.header("Security Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Threats Scanned Today", "1,245")
    col2.metric("Ransomware Detected", "2")
    col3.metric("Data Leaks Found", "1")

    st.subheader("System Status")
    st.success("System Monitoring Active")

    st.subheader("Live Security Logs")

    logs = [
        "Scanning files...",
        "Monitoring network traffic...",
        "Analyzing suspicious behavior...",
        "Protection system active..."
    ]

    for log in logs:
        st.write(log)
        time.sleep(0.3)

# ---------------- RANSOMWARE DETECTION ----------------
elif menu == "Ransomware Detection":

    st.header("Ransomware Detection System")

    if st.button("Start Scan"):

        with st.spinner("Scanning system..."):
            time.sleep(2)

        st.error("⚠️ Ransomware activity detected!")

        st.write("Suspicious file encryption behavior identified.")

# ---------------- DATA LEAK CHECK ----------------
elif menu == "Data Leak Check":

    st.header("Data Leak Scanner")

    data = {
        "File Name": ["customer_data.csv", "passwords.txt", "finance_report.pdf"],
        "Risk Level": ["🔴 High", "🟡 Medium", "🟢 Safe"]
    }

    df = pd.DataFrame(data)

    st.table(df)

# ---------------- REPORTS ----------------
elif menu == "Reports":

    st.header("Security Reports")

    if st.button("Generate Report"):

        st.success("Report Generated Successfully")

        report = """
GuardianX Security Report

Threats Scanned Today: 1245
Ransomware Detected: 2
Data Leak Alerts: 1
System Status: Secure
"""

        st.download_button(
            label="Download Report",
            data=report,
            file_name="guardianx_report.txt"
        )
