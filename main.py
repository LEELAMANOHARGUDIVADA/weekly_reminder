import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import pandas as pd
import pytz
from dotenv import dotenv_values
from flask import Flask, jsonify, request

from db.db import connect_db
from utils.alert_history import get_all_alert_history, update_alert_history

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# config = dotenv_values()
config = {
    "BOT_WEBHOOK_URL": os.environ['bot_webhook_url'],
    "CHANNEL_WEBHOOK_URL": os.environ['channel_webhook_url'],
    "SMTP_PORT": os.environ['smtp_port'],
    "SENDER_ZOHO_PASSWORD": os.environ['sender_zoho_password'],
    "SENDER_ZOHO_EMAIL": os.environ['sender_zoho_email'],
    "SMTP_ZOHO_SERVER": os.environ['smtp_zoho_server']
}

emailData = json.load(open("data/alert_emails.json"))
app = Flask(__name__)
s = smtplib.SMTP(config['SMTP_ZOHO_SERVER'], int(config['SMTP_PORT']))
s.starttls()
s.login(config['SENDER_ZOHO_EMAIL'], config['SENDER_ZOHO_PASSWORD'])

BOT_WEBHOOK_URL = config['BOT_WEBHOOK_URL']
CHANNEL_WEBHOOK_URL = config['CHANNEL_WEBHOOK_URL']

@app.route('/')
def index():
    return "SERVER IS UP AND RUNNING"

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
            logger.info(message['To'])
            s.send_message(message)
            update_alert_history(current_time=current_time, message=message, platform="Zoho")
        logger.info("Emails sent")
        return jsonify(success=True, message="Emails sent")
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
    connect_db()
    run_flask()
