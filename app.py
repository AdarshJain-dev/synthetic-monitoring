from flask import Flask, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

monitoring_jobs = {}

def check_url(url):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        response = requests.get(url, timeout=15, verify=False, allow_redirects=True)
        status = 'UP' if response.status_code == 200 else 'DOWN'
    except Exception as e:
        print(f"Error checking {url}: {e}")
        status = 'DOWN'
        
    monitoring_jobs[url]['status'] = status
    monitoring_jobs[url]['last_checked'] = now
    print(f"[{now}] {url} is {status}")

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        url = request.form["url"]
        interval = int(request.form["interval"])

        if url in monitoring_jobs:
            message = f"{url} is already being monitored."
        else:
            monitoring_jobs[url] = {"status": "Not Checked", "last_checked": "—"}
            scheduler.add_job(check_url, 'interval', [url], minutes=interval, id=url)
            message = f"Started monitoring {url} every {interval} minutes."

    # Convert dict to list for easier template rendering
    jobs = [
        {"url": url, "status": data["status"], "last_checked": data["last_checked"]}
        for url, data in monitoring_jobs.items()
    ]
    return render_template("index.html", jobs=jobs, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
