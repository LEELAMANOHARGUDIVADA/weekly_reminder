import requests
from datetime import datetime
import pytz
import logging
from utils.alert_history import update_alert_history
import schedule

logger = logging.getLogger()

def send_reminder(current_time, message, BOT_WEBHOOK_URL):
    payload = {
        "text": message
    }
    try:
        response = requests.post(BOT_WEBHOOK_URL, json=payload, verify=False)
        logger.info("Request sent")
        response.raise_for_status()
        update_alert_history(current_time=current_time, message=message, platform="CLIQ")
        logger.info("Reminder sent successfully")
    except requests.exceptions.RequestException as e:
        logger.error("Error sending reminder:", e)


def schedule_reminder(message, BOT_WEBHOOK_URL):
    ist = pytz.timezone('Asia/Kolkata')

    def reminder():
        current_time = datetime.now(ist)
        logger.info(current_time)
        if current_time.weekday() == 2 and current_time.hour == 16 and current_time.minute == 33:
            send_reminder(current_time, message, BOT_WEBHOOK_URL)

    schedule.every().minute.do(reminder)

