import schedule
import time
import requests
from datetime import datetime
import pytz
from dotenv import dotenv_values
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values(".env")

BOT_WEBHOOK_URL="https://cliq.zoho.in/company/60035345032/api/v2/bots/weeklyreminderbot/message?zapikey=1001.5d1368846882417b37751dd9b5f53094.cee8b02d5b2db0909ea7ea5153c2b826"
CHANNEL_WEBHOOK_URL="https://cliq.zoho.in/company/60035345032/api/v2/channelsbyname/weeklyreminder/message?zapikey=1001.5d1368846882417b37751dd9b5f53094.cee8b02d5b2db0909ea7ea5153c2b826"

def send_reminder():
    payload = {
        "text": "🔔 *Reminder*: Submit your timesheets today by EOD!"
    }
    try:
        # print("Entered")
        response = requests.post(CHANNEL_WEBHOOK_URL, json=payload, verify=False)
        print("Request sent")
        response.raise_for_status()
        print("Reminder sent successfully.")
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
