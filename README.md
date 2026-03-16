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
│── .gitignore                 # Git ignore rules
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

- Install dependencies:
```bash
pip install -r requirements.txt
```

- Set up environment variables in `.env`:
```env
NVIDIA_API_KEY="your_nvidia_api_key"
HIBP_API_KEY="your_haveibeenpwned_api_key"
```

- Run the backend:
```bash
python GuardianX-Backend/app.py
```

- Open `frontend.html` in a web browser to access the dashboard
🎤 Pitch Line
"GuardianX is not just a tool — it's your AI-powered guardian of the digital realm."
