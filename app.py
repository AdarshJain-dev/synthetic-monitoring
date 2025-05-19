from flask import Flask, request, render_template_string
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Simple HTML form for input
FORM = """
<h2>Synthetic Monitoring</h2>
<form method="POST">
  URL to monitor: <input name="url" type="text" required><br><br>
  Check frequency (minutes): 
  <select name="interval">
    <option value="15">Every 15 minutes</option>
    <option value="30">Every 30 minutes</option>
    <option value="60">Every 60 minutes</option>
  </select><br><br>
  <input type="submit" value="Start Monitoring">
</form>
<p>{{ message }}</p>
"""

# Monitor function
def check_url(url):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        if status == 200:
            print(f"[{now}] ✅ {url} is UP")
        else:
            print(f"[{now}] ❌ {url} returned status code {status}")
    except Exception as e:
        print(f"[{now}] ❌ ERROR checking {url}: {str(e)}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        interval = int(request.form["interval"])

        # Remove existing job (if any)
        scheduler.remove_all_jobs()

        # Schedule the new job
        scheduler.add_job(check_url, 'interval', [url], minutes=interval, id='monitor')

        return render_template_string(FORM, message=f"Started monitoring {url} every {interval} minutes.")
    return render_template_string(FORM, message="")
