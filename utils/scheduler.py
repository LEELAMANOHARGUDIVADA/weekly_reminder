import json
import requests
from datetime import datetime
import pytz
import logging
from dotenv import dotenv_values
import os
import schedule
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# BOT_WEBHOOK_URL = os.environ['bot_webhook_url']
# messages = json.load(open("../data/alert_messages.json"))
config = {
    "BOT_WEBHOOK_URL": os.environ['bot_webhook_url'],
    "CHANNEL_WEBHOOK_URL": os.environ['channel_webhook_url'],
    "SMTP_PORT": os.environ['smtp_port'],
    "SENDER_ZOHO_PASSWORD": os.environ['sender_zoho_password'],
    "SENDER_ZOHO_EMAIL": os.environ['sender_zoho_email'],
    "SMTP_ZOHO_SERVER": os.environ['smtp_zoho_server']
}

# config = dotenv_values()
def send_reminder(current_time, message, BOT_WEBHOOK_URL):
    payload = {
        "text": message
    }
    try:
        response = requests.post(BOT_WEBHOOK_URL, json=payload, verify=False)
        logger.info("Request sent")
        response.raise_for_status()
        # update_alert_history(current_time=current_time, message=message, platform="CLIQ")
        logger.info("Reminder sent successfully")
    except requests.exceptions.RequestException as e:
        logger.error("Error sending reminder:", e)


# def schedule_reminder(message, BOT_WEBHOOK_URL):
#     ist = pytz.timezone('Asia/Kolkata')
#
#     def reminder():
#         current_time = datetime.now(ist)
#         logger.info(current_time)
#
#         if current_time.weekday() == 4 and current_time.hour == 15 and current_time.minute == 59:
#             send_reminder(current_time, message, BOT_WEBHOOK_URL)
#
#     schedule.every().minute.do(reminder)

def should_send_reminder():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    logger.info(f"Current time: {current_time}")

    # Only send on Friday (weekday 4) at 15:59 IST
    return current_time.weekday() == 4 and current_time.hour == 19
if __name__ == "__main__":
    logger.info("Reminder bot started")
    if should_send_reminder():
        send_reminder(
            datetime.now(pytz.timezone('Asia/Kolkata')),
            "Reminder: Please Submit Timesheets Today By EOD",
            config['BOT_WEBHOOK_URL']
        )
    else:
        logger.info("Not the scheduled time. No reminder sent.")
