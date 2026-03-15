from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app)  # allow frontend to call backend

# ---------- Routes ----------
@app.route("/")
def home():
    return "GuardianX is live!"

# ---------- Dummy Security Data ----------
security_data = {
    "threats_scanned": 1245,
    "ransomware_detected": 2,
    "data_leaks_found": 1,
    "system_status": "Secure"
}

logs = [
    "Scanning file system for anomalies...",
    "Checking outbound network traffic...",
    "Analyzing process encryption patterns...",
    "Monitoring registry modifications..."
]

leak_data = [
    {"file": "customer_data.csv", "type": "CSV", "size": "24.3 MB", "risk": "High", "status": "Exposed"},
    {"file": "passwords.txt", "type": "TXT", "size": "1.2 KB", "risk": "Medium", "status": "Review"},
    {"file": "finance_report.pdf", "type": "PDF", "size": "8.7 MB", "risk": "Safe", "status": "Secured"}
]

# ---------- API Endpoints ----------
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    return jsonify(security_data)

@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify({
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "logs": logs
    })

@app.route("/api/scan", methods=["POST"])
def scan_system():
    return jsonify({
        "status": "alert",
        "message": "⚠️ Ransomware Activity Detected!",
        "details": "Suspicious file encryption behavior identified."
    })

@app.route("/api/leaks", methods=["GET"])
def leaks():
    return jsonify(leak_data)

@app.route("/api/report", methods=["GET"])
def report():
    report_text = """GuardianX Security Report
Threats Scanned: 1245
Ransomware Detected: 2
Data Leak Alerts: 1
System Status: Secure
"""
    return jsonify({"report": report_text})

# ---------- Run Server ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
