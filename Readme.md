# 🌐 Synthetic Website Uptime Monitoring Tool

A full-stack Flask web application for real-time uptime monitoring of websites, integrated with email alerts, failure thresholds, and DevOps practices including CI/CD and Docker deployment.

---

## 🔍 Project Overview

This project is designed to:

- Continuously monitor website endpoints.
- Trigger email alerts after a set number of failures.
- Provide a sleek web dashboard for managing URLs.
- Run in a background thread without blocking the UI.
- Integrate with CI/CD pipelines and run in containers.

---

## 🛠️ Tech Stack

| Layer         | Tools Used                     |
|---------------|--------------------------------|
| Backend       | Python, Flask                  |
| Frontend      | Bootstrap (via CDN), Jinja2    |
| Database      | SQLite                         |
| Email Alerts  | SMTP (Gmail/Custom)            |
| Monitoring    | `requests`, background thread  |
| DevOps        | Docker, GitHub Actions         |
| Deployment    | Docker Hub / Railway / EC2     |

---

## 🚀 How to Run

### 📍 Locally

```bash
git clone https://github.com/AdarshJain-dev/synthetic-monitoring.git
cd synthetic-monitoring
pip install -r requirements.txt
python app.py


Using Docker

# Build image
docker build -t synthetic-monitor .

# Run container
docker run -d -p 5000:5000 synthetic-monitor

synthetic-monitoring/
├── app.py
├── db.py
├── monitor.py
├── config.py
├── requirements.txt
├── Dockerfile
├── templates/
│   └── index.html
└── .github/
    └── workflows/
        └── deploy.yml
