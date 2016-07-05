import sqlite3

def read_db(db_name, table_name='Samples'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("select * from {}".format(table_name))
    my_table = cur.fetchall()
    conn.close()
    return my_table