import json
import sqlite3
import threading
from datetime import datetime
from email.mime.text import MIMEText
import pytz
import schedule
import time
from dotenv import dotenv_values
import urllib3
import smtplib
from flask import Flask, jsonify, request
import pandas as pd
from constants.db_queries import create_table
from db.db import connect_db
from utils.scheduler import schedule_reminder
from utils.alert_history import update_alert_history, get_all_alert_history
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

@app.route('/send-emails', methods=['POST'])
def send_emails():
    if "file" not in request.files:
        return jsonify(success=False, message="No File Found"), 400
    file = request.files['file']
    df = pd.read_csv(file, encoding='ISO-8859-1')
    emails = df['Email']
    if len(emails) == 0:
        return jsonify(success=False, message="No Emails Found")
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    try:

        for email in emails:
            message = MIMEText(emailData['emails'][0]['message'])
            message['Subject'] = emailData['emails'][0]['subject']
            message['From'] = config['SENDER_ZOHO_EMAIL']
            message['To'] = email
            # print(message['To'])
            logger.info(message['To'])
            s.send_message(message)
        update_alert_history(current_time=current_time, message=message, platform="Zoho")
        logger.info("Emails sent")
        return  jsonify(success=True, message="Emails sent")
    except smtplib.SMTPException as e:
        return jsonify(success=False, message=str(e))

@app.route('/alert-history', methods=['GET'])
def get_alert_history():
    data = get_all_alert_history()
    return jsonify(success=True, history=data)

def run_flask():
    logger.info("Flask App Running")
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    logger.info("Reminder bot started")
    connect_db()
    schedule_reminder(messages['messages'][0]['weekly_reminder'], BOT_WEBHOOK_URL)
    thread = threading.Thread(target=run_flask)
    thread.daemon = True
    thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)
