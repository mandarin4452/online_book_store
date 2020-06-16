import sqlite3

conn = sqlite3.connect('database.db')

cur = conn.cursor()
cur.execute(''' create table carts (email text, title text, link text, imageUrl text, price text, url text, author text);''')
conn.commit()
conn.close()