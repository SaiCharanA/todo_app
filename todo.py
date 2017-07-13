from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adavenisaicharan@gmail.com'
app.config['MAIL_PASSWORD'] = 'sai1020143151'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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

@app.route("/forgotpassword")
def forgotpassword():
	return render_template("forgotpassword.html")


######################################################################
#@app.route("/emailpassword",methods=['POST'])
#def emailpassword():
#	try:
#		conn = sqlite3.connect(todolist.db)
#		cur = conn.cursor
#		email = request.form["email"]


#		msg = "Your password to sign in into todo app is" + pwd
#	return ('sent')
######################################################################
@app.route("/signupdetails",methods=['POST'])
def signupdetails():
	try:
		conn = sqlite3.connect("todolist.db")
		cur = conn.cursor()
		username = request.form["username"]
		email = request.form["email"]
		password = request.form["password"]
		cur.execute("insert into signup (username,email,password) values (?,?,?)", [username,email,password])
		conn.commit()
		msg  = "User createsd successfully"
	except:
		conn.rollback()
		msg = "Error in creating user"
	finally:
		flash (msg)
		return render_template("signin.html")

######################################################################
#@app.route("/signindetails",methods=['POST'])
#def signindetails():
#	try:
#		conn = sqlite3.connect("todolist.db")
#		cur = conn.cursor()
#		email = request.form["username"]
#		pwd = request.form["password"]

#		return 'login successful'
######################################################################
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

#######################################################################
@app.route("/createdlist")
def createdlist():	
   		conn = sqlite3.connect("todolist.db")
   		conn.row_factory = sqlite3.Row
   		
   		cur = conn.cursor()
   		cur.execute("select * from list")
    	
		rows = cur.fetchall()
   		return render_template("createdlist.html",rows = rows)
   		conn.close()

#######################################################################
#@app.route("/edittask")
#def edittask():








#		return ('task updated')

#######################################################################
#@app.route("/deletetask")
#def deletetask():


#		return ('task deleted')


if __name__ == "__main__ ":
	app.run(debug=True)



