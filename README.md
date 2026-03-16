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
│── frontend.html              # Main Marvel-themed web dashboard
│── GuardianX-Backend/
│   └── app.py                 # Flask API server with AI features
│── requirements.txt           # Python dependencies
│── deploy.py                  # Deployment automation script
│── test.py                    # Pre-deployment testing script
│── .env                       # Environment variables (API keys)
│── .env.example               # Environment template
│── .gitignore                 # Git ignore rules
│── README.md                  # This file


🎯 Impact & SDG Alignment
- SDG 9 – Industry, Innovation & Infrastructure
- SDG 16 – Peace, Justice & Strong Institutions
GuardianX strengthens digital infrastructure and protects privacy, empowering individuals and organizations to stay safe in the digital era.
📖 How to Run
📖 How to Run & Deploy

### Local Development
```bash
# Clone and setup
git clone https://github.com/Guardian-X-048/GuardianX.git
cd GuardianX

# Configure environment
cp .env.example .env
# Edit .env with your actual API keys

# Install dependencies
pip install -r requirements.txt

# Run locally
python deploy.py local
```

### Production Deployment

#### Option 1: Render.com (Recommended)
```bash
# Prepare deployment package
python deploy.py render

# Upload the 'deploy/' folder to Render.com
# Set environment variables in Render dashboard:
# - NVIDIA_API_KEY
# - HIBP_API_KEY
# - FLASK_ENV=production
```

#### Option 2: Heroku
```bash
# Create Procfile if deploying to Heroku
echo "web: gunicorn GuardianX-Backend.app:app" > Procfile

# Deploy using Heroku CLI
heroku create your-guardianx-app
heroku config:set NVIDIA_API_KEY=your_key
heroku config:set HIBP_API_KEY=your_key
git push heroku main
```

#### Option 3: Railway/Vercel
- Upload the entire project
- Set environment variables in dashboard
- Use `python GuardianX-Backend/app.py` as start command

### Testing Before Deployment
```bash
# Run comprehensive tests
python test.py

# Start backend in background for testing
python deploy.py local &
# Then run tests
python test.py
```

## 🔐 Security Notes
- Never commit `.env` files to version control
- Keep API keys secure and rotate them regularly
- The application includes security headers and input validation
- All sensitive data is stored locally in SQLite database
- CORS is properly configured for frontend-backend communication
- Production mode uses Waitress WSGI server for better performance
🎤 Pitch Line
"GuardianX is not just a tool — it's your AI-powered guardian of the digital realm."
