from contextlib import closing
import psycopg2

lat = 0.0
lon = 0.0
tr_id = "1010040815020606"

conn = psycopg2.connect(dbname='db1', user='admin',
                        password='Q314ztb812', host='localhost')
cursor = conn.cursor()
command = "UPDATE api_scooter SET latitude={}, longitude={} WHERE tracker_id = '{}';".format(lat, lon, tr_id)
cursor.execute(command)
conn.commit()
