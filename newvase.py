import sqlite3

conn = sqlite3.connect('errors.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE errors (error text, word text)')