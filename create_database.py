import sqlite3

####################################################
conn = sqlite3.connect('todolist.db')
print("Opened database successfully")

conn.execute('CREATE TABLE list(id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)')
print("table created successfully")

conn.close()
####################################################
