create_table = """CREATE TABLE IF NOT EXISTS alerts
                  (
                      id         INTEGER PRIMARY KEY AUTOINCREMENT,
                      message    VARCHAR(255),
                      alert_date DATE,
                      platform   VARCHAR(20)
                  ) \
               """

insert_alert = """
               INSERT INTO alerts(message, alert_date, platform)
               VALUES (?, ?, ?) \
               """

get_all_alerts = "SELECT * FROM alerts"
