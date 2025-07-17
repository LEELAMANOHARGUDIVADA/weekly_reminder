from email.mime.text import MIMEText
import schedule
import time
import requests
from datetime import datetime
import pytz
from dotenv import dotenv_values
import urllib3
import smtplib
from flask import Flask, jsonify, request
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values()

app = Flask(__name__)
s = smtplib.SMTP(config['SMTP_ZOHO_SERVER'], int(config['SMTP_PORT']))
s.starttls()
s.login(config['SENDER_ZOHO_EMAIL'], config['SENDER_ZOHO_PASSWORD'])

BOT_WEBHOOK_URL=config['BOT_WEBHOOK_URL']
CHANNEL_WEBHOOK_URL=config['CHANNEL_WEBHOOK_URL']

def send_reminder():
    payload = {
        "text": "🔔 *Reminder*: Submit your timesheets today by EOD!"
    }
    try:
        # print("Entered")
        response = requests.post(CHANNEL_WEBHOOK_URL, json=payload, verify=False)
        print("Request sent")
        response.raise_for_status()
        print("Reminder sent successfully")
    except requests.exceptions.RequestException as e:
        print("Error sending reminder:", e)

def schedule_reminder():
    ist = pytz.timezone('Asia/Kolkata')

    def reminder():
        current_time = datetime.now(ist)
        print(current_time)
        if current_time.weekday() == 4 and current_time.hour == 19 and current_time.minute == 0:
            send_reminder()

    schedule.every().minute.do(reminder)


@app.route('/send-emails', methods=['POST'])
def send_emails():
    if "file" not in request.files:
        return jsonify(success=False, message="No File Found"), 400
    file = request.files['file']
    df = pd.read_csv(file, encoding='ISO-8859-1')
    emails = df['Email']
    if len(emails) == 0:
        return jsonify(success=False, message="No Emails Found")
    try:

        for email in emails:
            message = MIMEText("""
                Hi,

                You haven't submitted your timesheet this week. Please submit it as soon as possible.

                Thank you
            """)
            message['Subject'] = "Timesheet Not Submitted"
            message['From'] = config['SENDER_ZOHO_EMAIL']
            message['To'] = email
            print(message['To'])
            s.send_message(message)
        print("Emails sent")
        return  jsonify(success=True, message="Emails sent")
    except smtplib.SMTPException as e:
        return jsonify(success=False, message=str(e))


if __name__ == "__main__":
    print("Reminder bot started")
    schedule_reminder()
    app.run(debug=True)

    while True:
        schedule.run_pending()
        time.sleep(1)
