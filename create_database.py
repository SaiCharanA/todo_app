import sqlite3

####################################################
conn = sqlite3.connect('todolist.db')
print("Opened database successfully")

conn.execute('CREATE TABLE list(task TEXT)')
print("table created successfully")

conn.close()
####################################################
