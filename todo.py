from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route ("/")
def index():
	return render_template("index.html")

@app.route("/signup")
def signup():
	return render_template("signup.html")

@app.route("/signin")
def signin():
	return render_template("signin.html")

@app.route("/createlist")
def createlist():
	return render_template("createlist.html")

@app.route("/tasks",methods=['POST'])
def tasks():
	try:
		conn = sqlite3.connect("todolist.db")
		cur = conn.cursor()
		current_task = request.form["task"]
		cur.execute("insert into list (task) values (?)", [current_task])
		conn.commit()
		msg = "Record successfully added"
	except:
		conn.rollback()
		msg="error in insert operation"
	finally:		
		return render_template("result.html",msg = msg)
		conn.close()

@app.route("/createdlist")
def createdlist():	
   		con = sqlite3.connect("todolist.db")
   		con.row_factory = sqlite3.Row
   		
   		cur = con.cursor()
   		cur.execute("select * from list")
    	
		rows = cur.fetchall()
   		return render_template("createdlist.html",rows = rows)
   		con.close()


if __name__ == "__main__ ":
	app.run(debug=True)



