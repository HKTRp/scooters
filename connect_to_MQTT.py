import paho.mqtt.client as mqtt
import json
from contextlib import closing
import psycopg2


base_url = 'scooteradminpanel.ru'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, sdf):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    modes = [0, 10, 15, 25]
    postgre_bool = ['false', 'true']
    data = json.loads(msg.payload.decode())
    tr_id = data['id']
    lat = data['lat']
    lon = data['lon']
    lamp = postgre_bool[int(data['lamp'])]
    lock = postgre_bool[int(data['slock'])]
    engine = postgre_bool[int(data['enb'])]
    mode = modes[int(data['gear'])]
    battery = data['ubat']
    with closing(psycopg2.connect(dbname='db1', user='admin', password='Q314ztb812', host="localhost")) as conn:
        with conn.cursor() as cursor:

            cursor.execute("SELECT * FROM api_scooter WHERE tracker_id = %s;", (tr_id, ))
            is_in_base = False
            for _ in cursor:
                is_in_base = True
            if is_in_base:
                print("in base", tr_id)
                command = """UPDATE api_scooter SET latitude=%s, longitude=%s, lamp=%s,
                 lock=%s, engine=%s, battery=%s WHERE tracker_id = %s;"""
                variables = (lat, lon, lamp, lock, engine, battery, tr_id)
                cursor.execute(command, variables)
                conn.commit()
                command = "UPDATE api_scooter SET speed_limit=%s WHERE tracker_id = %s;"
                variables = (mode, tr_id)
                cursor.execute(command, variables)
                conn.commit()
            else:
                print("not in base", tr_id)
                command = """INSERT INTO api_scooter (scooter_name, status, alert, latitude, 
                longitude, description, photo, tracker_id, speed_limit, lamp, engine, lock, battery) VALUES ( %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                variables = (tr_id, 'ON', 'OK', 0.0, 0.0, "Без описания",
                             "image.png", tr_id, mode, lamp, engine, lock, battery)
                cursor.execute(command, variables)
                conn.commit()



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()
client.tls_insecure_set(True)

client.connect("scooteradminpanel.ru", 8883, 60)

client.subscribe("scooter")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
