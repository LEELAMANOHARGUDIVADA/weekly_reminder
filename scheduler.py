import requests
from datetime import datetime
import pytz
from utils.alert_history import update_alert_history
import schedule

def send_reminder(current_time, message, BOT_WEBHOOK_URL):
    payload = {
        "text": message
    }
    try:
        # print("Entered")
        response = requests.post(BOT_WEBHOOK_URL, json=payload, verify=False)
        print("Request sent")
        response.raise_for_status()
        update_alert_history(current_time=current_time, message=message, platform="Cliq")
        print("Reminder sent successfully")
    except requests.exceptions.RequestException as e:
        print("Error sending reminder:", e)


def schedule_reminder(message, BOT_WEBHOOK_URL):
    ist = pytz.timezone('Asia/Kolkata')

    def reminder():
        current_time = datetime.now(ist)
        print(current_time)
        if current_time.weekday() == 1 and current_time.hour == 16 and current_time.minute == 15:
            send_reminder(current_time, message, BOT_WEBHOOK_URL)

    schedule.every().minute.do(reminder)

