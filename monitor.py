import requests
from db import update_endpoint, reset_failures, get_all_endpoints
from config import EMAIL_FROM, EMAIL_TO, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD, FAILURE_THRESHOLD, CHECK_INTERVAL
import smtplib
from email.message import EmailMessage
import time

def send_email_alert(name, url):
    msg = EmailMessage()
    msg['Subject'] = f'[ALERT] {name} is Down'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content(f'The URL {url} appears to be down.')
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

def monitor_job():
    while True:
        endpoints = get_all_endpoints()
        for endpoint in endpoints:
            id, name, url, failures, _ = endpoint
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    reset_failures(id)
                else:
                    failures += 1
                    update_endpoint(id, failures)
                    if failures == FAILURE_THRESHOLD:
                        send_email_alert(name, url)
            except:
                failures += 1
                update_endpoint(id, failures)
                if failures == FAILURE_THRESHOLD:
                    send_email_alert(name, url)
        time.sleep(CHECK_INTERVAL)