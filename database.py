import sqlite3
import desc

db = sqlite3.connect('conversations.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE message
               (message text)''')