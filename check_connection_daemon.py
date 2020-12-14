import time
from datetime import datetime
from contextlib import closing
import psycopg2

while True:

    with closing(psycopg2.connect(dbname='db1', user='admin', password='Q314ztb812', host="localhost")) as conn:
        with conn.cursor() as cursor:
            to_exec = []
            cursor.execute("SELECT id, last_ping, alert_status FROM api_scooter;")
            for row in cursor:
                if row[2] != 'LC':
                    if datetime.now().timestamp() - row[1].timestamp() > 36000:
                        to_exec.append(row[0])
            conn.commit()
            for i in to_exec:
                cursor.execute("UPDATE api_scooter SET alert_status=%s WHERE id = %s", ('LC', i))
                conn.commit()
                cursor.execute("INSERT INTO api_alert (alert_type, alert_owner_id, alert_order_id, gotten ) "
                               "VALUES (%s, %s, %s, %s);", ('LC', i, 1, datetime.today()))
                conn.commit()
    time.sleep(180)
