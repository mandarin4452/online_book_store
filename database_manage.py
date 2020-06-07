import sqlite3

conn = sqlite3.connect('database.db')

cur = conn.cursor()

cur.execute(''' create table members (email text, password text, name text, phone_number text);''')
conn.commit()
conn.close()