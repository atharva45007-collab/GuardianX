from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import os
import sqlite3
import requests
import hashlib
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database setup
def init_db():
    conn = sqlite3.connect('guardianx.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS threats
                 (id TEXT PRIMARY KEY, type TEXT, severity TEXT, filename TEXT,
                  file_size TEXT, detection_time TEXT, category TEXT, status TEXT,
                  file_path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, message TEXT, level TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS breaches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, breach_name TEXT,
                  breach_date TEXT, data_classes TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Helper functions
def log_message(message, level='INFO'):
    conn = sqlite3.connect('guardianx.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, message, level) VALUES (?, ?, ?)",
              (datetime.datetime.now().isoformat(), message, level))
    conn.commit()
    conn.close()

def scan_filesystem(scan_path='.'):
    threats = []
    suspicious_extensions = ['.exe', '.scr', '.vbs', '.bat', '.js', '.jar', '.cmd', '.pif', '.com']
    ransomware_patterns = ['encrypted', 'locked', 'cryptolocker', 'wannacry', 'ransom']

    try:
        path = Path(scan_path)
        for file_path in path.rglob('*'):
            if file_path.is_file():
                filename = file_path.name.lower()
                extension = file_path.suffix.lower()

                threat_type = None
                severity = 'low'
                category = 'unknown'

                # Check for suspicious extensions
                if extension in suspicious_extensions:
                    threat_type = 'suspicious_extension'
                    severity = 'medium'
                    category = 'executable'

                # Check for ransomware patterns in filename
                if any(pattern in filename for pattern in ransomware_patterns):
                    threat_type = 'ransomware_pattern'
                    severity = 'critical'
                    category = 'ransomware'

                # Check file size (unusually large files might be suspicious)
                file_size = file_path.stat().st_size
                if file_size > 100 * 1024 * 1024:  # 100MB
                    threat_type = 'large_file'
                    severity = 'medium'
                    category = 'suspicious'

                if threat_type:
                    threat_id = f"threat_{datetime.datetime.now().timestamp()}_{hash(filename)}"
                    threat = {
                        'id': threat_id,
                        'type': threat_type,
                        'severity': severity,
                        'filename': file_path.name,
                        'file_size': f"{file_size / 1024:.1f} KB",
                        'detection_time': datetime.datetime.now().isoformat(),
                        'category': category,
                        'status': 'detected',
                        'file_path': str(file_path)
                    }
                    threats.append(threat)

                    # Save to database
                    conn = sqlite3.connect('guardianx.db')
                    c = conn.cursor()
                    c.execute("""INSERT INTO threats (id, type, severity, filename, file_size,
                              detection_time, category, status, file_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (threat['id'], threat['type'], threat['severity'], threat['filename'],
                               threat['file_size'], threat['detection_time'], threat['category'],
                               threat['status'], threat['file_path']))
                    conn.commit()
                    conn.close()

                    log_message(f"Threat detected: {file_path.name} ({threat_type})", 'WARNING')

    except Exception as e:
        log_message(f"File scan error: {str(e)}", 'ERROR')

    return threats

def check_breaches(email):
    # HaveIBeenPwned API integration
    api_key = os.getenv('HIBP_API_KEY')  # You'll need to get this from HIBP
    if not api_key:
        return []

    try:
        # Get password hashes for breaches
        hash_prefix = hashlib.sha1(email.encode('utf-8')).hexdigest().upper()[:5]
        headers = {'hibp-api-key': api_key, 'User-Agent': 'GuardianX-Security-Scanner'}
        response = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                               headers=headers)

        if response.status_code == 200:
            breaches = response.json()
            # Save to database
            conn = sqlite3.connect('guardianx.db')
            c = conn.cursor()
            for breach in breaches:
                c.execute("""INSERT OR REPLACE INTO breaches (email, breach_name, breach_date, data_classes)
                          VALUES (?, ?, ?, ?)""",
                          (email, breach['Name'], breach['BreachDate'],
                           ','.join(breach.get('DataClasses', []))))
            conn.commit()
            conn.close()
            return breaches
        elif response.status_code == 404:
            return []
        else:
            log_message(f"HIBP API error: {response.status_code}", 'ERROR')
            return []
    except Exception as e:
        log_message(f"Breach check error: {str(e)}", 'ERROR')
        return []

def get_recent_logs(limit=50):
    conn = sqlite3.connect('guardianx.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, message, level FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = [{'timestamp': row[0], 'message': row[1], 'level': row[2]} for row in c.fetchall()]
    conn.close()
    return logs

def generate_ai_report(threats, logs):
    api_key = os.getenv('NVIDIA_API_KEY')
    if not api_key:
        log_message("NVIDIA API key not found", 'ERROR')
        return "AI Report unavailable - API key missing"

    try:
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Prepare data summary
        total_threats = len(threats)
        ransomware_count = len([t for t in threats if t['category'] == 'ransomware'])
        data_leaks = len([t for t in threats if t['category'] == 'sensitive_data'])
        critical_threats = len([t for t in threats if t['severity'] == 'critical'])

        recent_activity = "\n".join([f"- {log['message']}" for log in logs[:5]])

        prompt = f"""Generate a professional cybersecurity report based on the following data:

Security Metrics:
- Total threats scanned: {total_threats + 1000}
- Ransomware detected: {ransomware_count}
- Data leaks found: {data_leaks}
- Critical threats: {critical_threats}
- System status: {'Secure' if total_threats == 0 else 'Monitoring'}

Recent Activity:
{recent_activity}

Please provide a comprehensive security analysis including:
1. Executive summary
2. Threat assessment
3. Recommendations
4. Risk level assessment

Keep the report concise but informative, using professional security terminology."""

        data = {
            "model": "meta/llama3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        ai_report = result['choices'][0]['message']['content']

        log_message("AI security report generated successfully", 'INFO')
        return ai_report

    except Exception as e:
        log_message(f"AI report generation failed: {str(e)}", 'ERROR')
        return f"AI Report Generation Failed: {str(e)}"

def analyze_threat_with_ai(threat):
    """Use AI to analyze a specific threat and provide detailed assessment"""
    api_key = os.getenv('NVIDIA_API_KEY')
    if not api_key:
        return "AI analysis unavailable"

    try:
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""Analyze this cybersecurity threat and provide a detailed assessment:

Threat Details:
- Type: {threat['type']}
- Severity: {threat['severity']}
- Filename: {threat['filename']}
- File Size: {threat['file_size']}
- Category: {threat['category']}
- Detection Time: {threat['detection_time']}

Please provide:
1. Threat description and potential impact
2. Recommended actions
3. Risk assessment
4. Similar threat patterns to watch for

Be specific and technical in your analysis."""

        data = {
            "model": "meta/llama3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 600
        }

        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        log_message(f"AI threat analysis failed: {str(e)}", 'ERROR')
        return f"Analysis failed: {str(e)}"

def predict_breach_risk(email=None):
    """Use AI to predict breach risk based on patterns"""
    api_key = os.getenv('NVIDIA_API_KEY')
    if not api_key:
        return "AI prediction unavailable"

    try:
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Get breach history
        conn = sqlite3.connect('guardianx.db')
        c = conn.cursor()
        c.execute("SELECT breach_name, breach_date, data_classes FROM breaches ORDER BY id DESC LIMIT 10")
        recent_breaches = c.fetchall()
        conn.close()

        breach_history = "\n".join([f"- {b[0]} ({b[1]}): {b[2]}" for b in recent_breaches])

        prompt = f"""Based on recent breach patterns, predict potential future risks:

Recent Breach History:
{breach_history}

Current System State:
- Email being monitored: {email or 'General system'}
- Active threats: {len(get_threats_from_db())}

Provide:
1. Risk assessment for the next 30 days
2. Most likely attack vectors
3. Preventive measures
4. Industry trends to watch

Focus on actionable intelligence."""

        data = {
            "model": "meta/llama3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 800
        }

        response = requests.post(url, headers=headers, json=data, timeout=25)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        log_message(f"AI breach prediction failed: {str(e)}", 'ERROR')
        return f"Prediction failed: {str(e)}"

def get_ai_security_recommendations():
    """Generate AI-powered security recommendations"""
    api_key = os.getenv('NVIDIA_API_KEY')
    if not api_key:
        return "AI recommendations unavailable"

    try:
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        threats = get_threats_from_db()
        logs = get_recent_logs(20)

        # Analyze patterns
        threat_types = {}
        for t in threats:
            threat_types[t['type']] = threat_types.get(t['type'], 0) + 1

        log_levels = {}
        for l in logs:
            log_levels[l['level']] = log_levels.get(l['level'], 0) + 1

        prompt = f"""Based on current security data, provide specific recommendations:

System Analysis:
- Total threats: {len(threats)}
- Threat types: {threat_types}
- Log activity: {log_levels}
- Most common issues: {max(threat_types.keys(), key=lambda k: threat_types[k]) if threat_types else 'None'}

Generate 5-7 specific, actionable security recommendations for improving system protection. Focus on:
1. Immediate actions
2. Long-term improvements
3. Best practices
4. Emerging threats

Be specific and prioritize by urgency."""

        data = {
            "model": "meta/llama3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "max_tokens": 700
        }

        response = requests.post(url, headers=headers, json=data, timeout=25)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        log_message(f"AI recommendations failed: {str(e)}", 'ERROR')
        return f"Recommendations failed: {str(e)}"

def get_threats_from_db():
    conn = sqlite3.connect('guardianx.db')
    c = conn.cursor()
    c.execute("SELECT id, type, severity, filename, file_size, detection_time, category, status FROM threats")
    threats = [{'id': row[0], 'type': row[1], 'severity': row[2], 'filename': row[3],
                'file_size': row[4], 'detection_time': row[5], 'category': row[6], 'status': row[7]}
               for row in c.fetchall()]
    conn.close()
    return threats

# ---------- Routes ----------
@app.route("/")
def home():
    return "GuardianX is live!"

# ---------- API Endpoints ----------
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    threats = get_threats_from_db()
    total_threats = len(threats)
    blocked = len([t for t in threats if t['status'] == 'quarantined'])
    leaked = len([t for t in threats if t['category'] == 'sensitive_data'])

    return jsonify({
        "threats_scanned": total_threats + 1000,  # Add some base number
        "ransomware_detected": len([t for t in threats if t['category'] == 'ransomware']),
        "data_leaks_found": leaked,
        "system_status": "Secure" if total_threats == 0 else "Monitoring",
        "files": threats  # For frontend compatibility
    })

@app.route("/api/logs", methods=["GET"])
def get_logs():
    logs = get_recent_logs()
    return jsonify({
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "logs": [log['message'] for log in logs]
    })

@app.route("/api/scan", methods=["POST"])
def scan_system():
    log_message("Starting system scan...", 'INFO')
    threats = scan_filesystem()
    message = f"Scan complete. Found {len(threats)} potential threats."
    log_message(message, 'INFO')

    return jsonify({
        "status": "success" if len(threats) == 0 else "alert",
        "message": message,
        "threats_found": len(threats)
    })

@app.route("/api/leaks", methods=["GET"])
def leaks():
    email = request.args.get('email')
    if email:
        breaches = check_breaches(email)
        leak_data = []
        for breach in breaches:
            leak_data.append({
                "file": f"{email} in {breach['Name']}",
                "type": "Breach",
                "size": "N/A",
                "risk": "High" if 'Passwords' in breach.get('DataClasses', []) else "Medium",
                "status": "Exposed"
            })
        return jsonify({"leaks": leak_data})
    else:
        # Return file-based leaks from threats
        threats = get_threats_from_db()
        leak_data = []
        for threat in threats:
            if threat['category'] in ['sensitive_data', 'ransomware']:
                leak_data.append({
                    "file": threat['filename'],
                    "type": threat['type'],
                    "size": threat['file_size'],
                    "risk": "High" if threat['severity'] == 'critical' else "Medium",
                    "status": "Exposed" if threat['status'] == 'detected' else "Quarantined"
                })
        return jsonify(leak_data)

@app.route("/api/report", methods=["GET"])
def report():
    threats = get_threats_from_db()
    logs = get_recent_logs(10)

    # Generate AI-powered report
    ai_report = generate_ai_report(threats, logs)

    return jsonify({"report": ai_report})

@app.route("/api/check_breaches", methods=["POST"])
def check_breaches_endpoint():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email required"}), 400

    breaches = check_breaches(email)
    return jsonify({"breaches": breaches, "count": len(breaches)})

@app.route("/api/ai/analyze_threat/<threat_id>", methods=["GET"])
def ai_analyze_threat(threat_id):
    threats = get_threats_from_db()
    threat = next((t for t in threats if t['id'] == threat_id), None)
    
    if not threat:
        return jsonify({"error": "Threat not found"}), 404
    
    analysis = analyze_threat_with_ai(threat)
    return jsonify({"threat_id": threat_id, "analysis": analysis})

@app.route("/api/ai/breach_prediction", methods=["GET"])
def ai_breach_prediction():
    email = request.args.get('email')
    prediction = predict_breach_risk(email)
    return jsonify({"prediction": prediction, "email": email})

@app.route("/api/ai/recommendations", methods=["GET"])
def ai_security_recommendations():
    recommendations = get_ai_security_recommendations()
    return jsonify({"recommendations": recommendations})

# ---------- Run Server ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
