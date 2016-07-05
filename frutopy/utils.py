import sqlite3
import psycopg2
from datetime import datetime


table_indices = {
    'spectrum': 1,
    'fruit': 2,
    'label': 3,
    'gps': 4,
    'tmstp': 5,
    'ml_model': 7,
    'sp_model': 8
}


def read_db(db_name, table_name='Samples'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("select * from {}".format(table_name))
    my_table = cur.fetchall()
    conn.close()
    return my_table


def write_central_db(rows):
    conn = psycopg2.connect(database='frutopy', user='berry', password='password123', host='localhost')  # FIXME please
    cur = conn.cursor()
    table_name = 'tables_sample'
    cur.execute("BEGIN;")
    for row in rows:
        a = "'{" + row[1] + "}'"
        #a = [float(i) for i in row[1].split(',')]
        cur.execute(
            """INSERT INTO %s (spectrum, fruit, label, gps, tmstp, ml_model_id, sp_model_id) VALUES (%s, %d, %d, '%s', '%s', %d, %d);"""
            % (table_name, a, row[2], row[3], "djkdsfjkdsfj", datetime.fromtimestamp(row[5]), row[6]+1, row[7]+1))
        conn.commit()
    cur.execute("COMMIT;")


#write_central_db(read_db('samples.db'))