import schedule
import time
import requests
from datetime import datetime
import pytz
from dotenv import dotenv_values
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values()

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

if __name__ == "__main__":
    print("Reminder bot started")
    schedule_reminder()

    while True:
        schedule.run_pending()
        time.sleep(1)
