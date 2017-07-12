from flask import Flask, render_template, request
import sqlite3 as sql

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

@app.route("/tasks",methods=['POST','GET'])
def tasks():
	if request.method =='POST':
		try:
			task = request.form["task"]
			with sql.connect("todolist.db") as conn:
				cur = conn.cursor()

				cur.execute("INSERT INTO list(task) VALUES(?)",(task))
				conn.commit()
				msg = "Record successfully added"
		except:
			conn.rollback()
			msg="error in insert operation"
		finally:
			msg = "Record successfully added"		
			return render_template("result.html")
			conn.close()

@app.route("/createdlist")
def createdlist():	
   		con = sql.connect("todolist.db")
   		con.row_factory = sql.Row
   		
   		cur = con.cursor()
   		cur.execute("select * from list")
    	
		rows = cur.fetchall();
   		return render_template("createdlist.html",rows = rows)
   		con.close()

if __name__ == "__main__ ":
	app.run(debug=True)



