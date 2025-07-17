# Cliq Weekly Reminder - TimeSheets

## Getting Started

1. Clone the repository
    ```
      git clone https://github.com/LEELAMANOHARGUDIVADA/weekly_reminder.git
   ```
2. Install required packages
    ```
      pip install requirements.txt
   ```
3. Add a .env file in the root directory
    ```
      BOT_WEBHOOK_URL="your-bot-webhook-url"
      CHANNEL_WEBHOOK_URL="your-channel-webhook-url"
      SMTP_PORT=587
      SENDER_ZOHO_PASSWORD="your-zoho-app-specific-password"
      SENDER_ZOHO_EMAIL="your-zoho-email"
      SMTP_ZOHO_SERVER=smtp.zoho.in
   ```
4. Run the application in the terminal
    ```
      python main.py
   ```