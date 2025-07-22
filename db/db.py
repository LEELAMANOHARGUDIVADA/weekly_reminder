import sqlite3
from constants.db_queries import create_table
import logging

logger = logging.getLogger()

def connect_db():
    try:
        conn = sqlite3.connect('alerts.db', check_same_thread=False)
        logger.info("Connected to database")
        cursor = conn.cursor()
        cursor.execute(create_table)
        conn.commit()
    except Exception as e:
        logger.error("Error Connecting to database: ", e)