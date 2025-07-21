import json
import threading
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

messages = json.load(open("data/alert_messages.json"))
emailData = json.load(open("data/alert_emails.json"))
app = Flask(__name__)
s = smtplib.SMTP(config['SMTP_ZOHO_SERVER'], int(config['SMTP_PORT']))
s.starttls()
s.login(config['SENDER_ZOHO_EMAIL'], config['SENDER_ZOHO_PASSWORD'])

BOT_WEBHOOK_URL=config['BOT_WEBHOOK_URL']
CHANNEL_WEBHOOK_URL=config['CHANNEL_WEBHOOK_URL']

def send_reminder(current_time, message):
    payload = {
        "text": message
    }
    try:
        # print("Entered")
        response = requests.post(BOT_WEBHOOK_URL, json=payload, verify=False)
        print("Request sent")
        response.raise_for_status()
        update_alert_history(current_time=current_time, message=message)
        print("Reminder sent successfully")
    except requests.exceptions.RequestException as e:
        print("Error sending reminder:", e)

def schedule_reminder():
    ist = pytz.timezone('Asia/Kolkata')

    def reminder():
        current_time = datetime.now(ist)
        print(current_time)
        if current_time.weekday() == 0 and current_time.hour == 19 and current_time.minute == 46:
            send_reminder(current_time, messages['messages'][0])

    schedule.every().minute.do(reminder)

def update_alert_history(current_time, message):
    data = json.load(open('data/alert_history.json'))
    data['history'].append({
        "id": data['history'][-1]['id'] + 1,
        "message": message,
        "alert_date": str(current_time)
    })
    with open('data/alert_history.json', 'w') as file:
        json.dump(data, file)
        print("Alert History Updated")
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
            message = MIMEText(emailData['emails'][0]['message'])
            message['Subject'] = emailData['emails'][0]['subject']
            message['From'] = config['SENDER_ZOHO_EMAIL']
            message['To'] = email
            print(message['To'])
            s.send_message(message)
        print("Emails sent")
        return  jsonify(success=True, message="Emails sent")
    except smtplib.SMTPException as e:
        return jsonify(success=False, message=str(e))

def run_flask():
    print("Flask App Running")
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    print("Reminder bot started")
    schedule_reminder()
    thread = threading.Thread(target=run_flask)

    thread.daemon = True
    thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)
