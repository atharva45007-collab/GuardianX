from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import os
import sqlite3
import requests
import hashlib
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- Security Headers ----------------
@app.after_request
def add_security_headers(response):
    """Add essential security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# ---------------- API Key Validation ----------------
REQUIRED_KEYS = ['INTELX_API_KEY']
missing_keys = [key for key in REQUIRED_KEYS if not os.getenv(key)]

if missing_keys:
    print("⚠ WARNING: Missing or placeholder API keys detected!")
    print(f"Missing keys: {', '.join(missing_keys)}")
    print("Please set up your .env file with actual API keys.")
    print("See .env.example for required configuration.\n")

# ---------------- Database Setup ----------------
def init_db():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect('guardianx.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS threats
                 (id TEXT PRIMARY KEY, type TEXT, severity TEXT, filename TEXT,
                  file_size TEXT, detection_time TEXT, category TEXT, status TEXT,
                  file_path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, message TEXT, level TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS intelx_results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, result_count INTEGER,
                  timestamp TEXT, data TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ---------------- Helper Functions ----------------
def log_message(message, level='INFO'):
    """Log messages into the database."""
    conn = sqlite3.connect('guardianx.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, message, level) VALUES (?, ?, ?)",
              (datetime.datetime.now().isoformat(), message, level))
    conn.commit()
    conn.close()

def scan_filesystem(scan_path='.'):
    """Scan the filesystem for suspicious files."""
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

                # Detect suspicious extensions
                if extension in suspicious_extensions:
                    threat_type = 'suspicious_extension'
                    severity = 'medium'
                    category = 'executable'

                # Detect ransomware patterns
                if any(pattern in filename for pattern in ransomware_patterns):
                    threat_type = 'ransomware_pattern'
                    severity = 'critical'
                    category = 'ransomware'

                # Detect unusually large files
                file_size = file_path.stat().st_size
                if file_size > 100 * 1024 * 1024:  # >100MB
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

                    # Save to DB
                    conn = sqlite3.connect('guardianx.db')
                    c = conn.cursor()
                    c.execute("""INSERT INTO threats (id, type, severity, filename, file_size,
                                 detection_time, category, status, file_path)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (threat['id'], threat['type'], threat['severity'], threat['filename'],
                               threat['file_size'], threat['detection_time'], threat['category'],
                               threat['status'], threat['file_path']))
                    conn.commit()
                    conn.close()

                    log_message(f"Threat detected: {file_path.name} ({threat_type})", 'WARNING')

    except Exception as e:
        log_message(f"File scan error: {str(e)}", 'ERROR')

    return threats

# ---------------- IntelX Integration ----------------
def intelx_search(query):
    """
    Search IntelX for data leaks or exposures related to the query.
    Docs: https://intelx.io/docs
    """
    api_key = os.getenv('INTELX_API_KEY')
    if not api_key:
        log_message("IntelX API key not configured", 'ERROR')
        return {"error": "IntelX API key not configured"}

    headers = {
        "x-key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://2.intelx.io/intelligent/search",
            headers=headers,
            json={"term": query, "maxresults": 10, "media": 0}
        )

        if response.status_code != 200:
            log_message(f"IntelX API error: {response.text}", 'ERROR')
            return {"error": "IntelX API request failed"}

        data = response.json()
        result_count = len(data.get("records", []))

        # Save results to DB
        conn = sqlite3.connect('guardianx.db')
        c = conn.cursor()
        c.execute("""INSERT INTO intelx_results (query, result_count, timestamp, data)
                     VALUES (?, ?, ?, ?)""",
                  (query, result_count, datetime.datetime.now().isoformat(), str(data)))
        conn.commit()
        conn.close()

        log_message(f"IntelX search completed for '{query}' with {result_count} results.", 'INFO')
        return {"query": query, "result_count": result_count, "data": data}

    except Exception as e:
        log_message(f"IntelX search error: {str(e)}", 'ERROR')
        return {"error": str(e)}

# ---------------- API Endpoints ----------------
@app.route("/api/intelx/search", methods=["POST"])
def intelx_search_endpoint():
    """Endpoint to perform IntelX search for a given query."""
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    results = intelx_search(query)
    return jsonify(results)

@app.route("/api/scan", methods=["GET"])
def scan_endpoint():
    """Trigger a filesystem scan."""
    threats = scan_filesystem('.')
    return jsonify({"threats_detected": len(threats), "details": threats})

# ---------------- Run Server ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if os.environ.get('FLASK_ENV') == 'production':
        from waitress import serve
        print(f"🚀 Starting GuardianX in production mode on port {port}")
        serve(app, host="0.0.0.0", port=port)
    else:
        print(f"🛠 Starting GuardianX in development mode on port {port}")
        app.run(host="0.0.0.0", port=port, debug=True)
