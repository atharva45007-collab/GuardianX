📌 Overview
GuardianX is a next‑gen cybersecurity solution designed to protect digital identities. It detects ransomware activity and alerts users about personal data leaks in real time using AI-powered analysis and real-time monitoring.
🚀 Features
- **Real File System Scanning** – Scans directories for suspicious files, extensions, and ransomware patterns
- **AI-Powered Threat Analysis** – Uses NVIDIA AI to provide detailed threat assessments and recommendations
- **Data Breach Detection** – Integrates with HaveIBeenPwned API to check credential exposure
- **AI Security Reports** – Generates intelligent security reports using advanced language models
- **Breach Risk Prediction** – AI-powered predictions of future security risks
- **Persistent Data Storage** – SQLite database for threat logs and breach history
- **Real-time Monitoring** – Continuous system activity logging and analysis
- **User‑Friendly GUI** – Clean dashboard with alerts, breach details, and severity indicators
🧑‍💻 Team – DarkVibe Coders (BBDU Lucknow)
- Aditya Singh – Team Lead / Architect
- Anuj Gond – API Integration Specialist
- Anas Khan – GUI Designer
- Atharva Mishra – Documentation & Pitch Manager
- Aryan Kumar – Testing & Demo Handler
🛠️ Tech Stack
- **Backend**: Python Flask, SQLite, NVIDIA AI API, HaveIBeenPwned API
- **Frontend**: HTML/CSS/JavaScript, TailwindCSS, Lucide Icons
- **APIs**: NVIDIA AI Foundation Models, HaveIBeenPwned
- **Deployment**: Heroku/Gunicorn, Environment-based configuration
📂 Project Structure
GuardianX/
│── frontend.html              # Main web dashboard
│── GuardianX-Backend/
│   └── app.py                 # Flask API server with AI features
│── requirements.txt           # Python dependencies
│── Procfile                   # Heroku deployment config
│── .env                       # Environment variables (API keys)
│── .env.example               # Environment template
│── .gitignore                 # Git ignore rules
│── security_audit.py          # Security configuration checker
│── README.md                  # This file


🎯 Impact & SDG Alignment
- SDG 9 – Industry, Innovation & Infrastructure
- SDG 16 – Peace, Justice & Strong Institutions
GuardianX strengthens digital infrastructure and protects privacy, empowering individuals and organizations to stay safe in the digital era.
📖 How to Run
- Clone the repo:
```bash
git clone https://github.com/Guardian-X-048/GuardianX.git
cd GuardianX
```

- Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

- Get API Keys:
  - **NVIDIA AI**: Visit https://build.nvidia.com/ and get your API key
  - **HaveIBeenPwned**: Visit https://haveibeenpwned.com/API/Key for breach checking

- Install dependencies:
```bash
pip install -r requirements.txt
```

- Run the backend:
```bash
python GuardianX-Backend/app.py
```

- Open `frontend.html` in a web browser to access the dashboard

## 🔐 Security Notes
- Never commit `.env` files to version control
- Keep API keys secure and rotate them regularly
- The application includes security headers and input validation
- All sensitive data is stored locally in SQLite database
- Run `python security_audit.py` to check your security configuration
🎤 Pitch Line
"GuardianX is not just a tool — it's your AI-powered guardian of the digital realm."
