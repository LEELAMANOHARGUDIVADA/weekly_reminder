import json
import logging
import sqlite3

from constants.db_queries import insert_alert, get_all_alerts

logger = logging.getLogger()

conn = sqlite3.connect('../alerts.db', check_same_thread=False)
cursor = conn.cursor()

def update_alert_history(current_time, message, platform):
    try:
        cursor.execute(insert_alert, (str(message), str(current_time), platform))
        conn.commit()
        logger.info("Alert History Updated")
    except Exception as e:
        logger.error("Error updating alert history: ", e)


def get_all_alert_history():
    try:
        cursor.execute(get_all_alerts)
        return cursor.fetchall()
    except Exception as e:
        logger.error("Error getting alert history: ", e)