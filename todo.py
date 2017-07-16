from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)
app.secret_key = 'its a secret key'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'todoapp.cc@gmail.com'
app.config['MAIL_PASSWORD'] = 'sai1020143151'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

loggedin_username = ''
loggedin_email = ''

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
	if (loggedin_email == ''):
		msg = "Please login to create a task"
		return render_template("signin.html",msg = msg)
	else:
		return render_template("createlist.html",loggedin_username = loggedin_username)

@app.route("/forgotpassword")
def forgotpassword():
	return render_template("forgotpassword.html")


######################################################################
@app.route("/emailpassword",methods=['POST'])
def emailpassword():
	conn = sqlite3.connect("todolist.db")
	cur = conn.cursor()
	email = request.form["email"]
	cur.execute("select * from signup where email = ?",(email,))
	row = cur.fetchone()
	if not row:
		msg = "Email not registered or email entered  wrongly"
		return render_template("signup.html",msg = msg)
	else :
		pwd = row[2]
		msg = Message('Todo app password', sender = 'todoapp.cc@gmail.com', recipients = [email])
		msg.body = "Your password to sign in into todo app is " + pwd
		mail.send(msg)
		mesg = 'Please Check your email for password'
	   	return render_template("signin.html",msg=mesg)
	   	conn.close()

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
		msg  = "User created successfully"
	except:
		conn.rollback()
		msg = "Error in creating user.Looks like email already registered!"
	finally:
		return render_template("signin.html",msg=msg)

######################################################################
@app.route("/signincheckup",methods=['POST'])
def signincheckup():
	try:
		global loggedin_username
		global loggedin_email
		conn = sqlite3.connect("todolist.db")
		cur = conn.cursor()

		email = request.form["email"]
		pwd = request.form["password"]
		
		cur.execute("select * from signup where email = ?", (email,))
		row = cur.fetchone()
		if not row:
			msg = "User doesn't exist.Please register to continue"
			return render_template("signup.html",msg = msg)
		else:
			query = row[2]
			if (query == pwd):
				cur.execute("select * from signup where email = ?", (email,) )
				loggedin_username = cur.fetchone()[0]
				loggedin_email = email
				return render_template("signedin.html",loggedin_username = loggedin_username)	
			else:
				msg = "Please check your mail and password again"
				return render_template("signin.html",msg = msg)

	except:
		conn.rollback()
		msg = 'error in connection'
	finally:
		conn.close()

######################################################################
@app.route("/tasks",methods=['POST'])
def tasks():
	global loggedin_email
	if (loggedin_email != ''):
		try:
			conn = sqlite3.connect("todolist.db")
			cur = conn.cursor()
			current_task = request.form["task"]

			cur.execute("insert into list (email,task) values (?,?)", (loggedin_email,current_task))
			conn.commit()
			msg = "Record successfully added"
		except:
			conn.rollback()
			msg = "error in insert operation"
		finally:		
			return render_template("result.html",msg = msg,loggedin_username = loggedin_username)
			conn.close()
	else:
		msg =  "Please login to create a task"
   		return render_template("signin.html",msg = msg)

#######################################################################
@app.route("/createdlist")
def createdlist():
	global loggedin_email
	if (loggedin_email != '') :	
   		conn = sqlite3.connect("todolist.db")
   		conn.row_factory = sqlite3.Row
   		
   		cur = conn.cursor()
   		cur.execute("select * from list where email = ?", (loggedin_email,) )
   		list_rows = cur.fetchall()
		cur.execute("select * from completedtasks where email = ?", (loggedin_email,) )
		completed_rows = cur.fetchall()
		cur.execute("select * from deletedtasks where email = ?", (loggedin_email,) )
		deleted_rows = cur.fetchall()
		return render_template("createdlist.html",list_rows = list_rows,completed_rows=completed_rows,deleted_rows=deleted_rows,loggedin_username = loggedin_username)
		conn.close()
   	else:
   		msg = "Please login to show your list of tasks"
   		return render_template("signin.html",msg = msg)

#######################################################################
@app.route("/updatetask",methods=['POST'])
def updatetask():
	try:
		taskid = request.form['taskid']
		updatedtask = request.form['updatedtask']
		conn = sqlite3.connect("todolist.db")
		cur = conn.cursor()
		cur.execute("update list set task = ? where id = ?",(updatedtask,taskid))

		conn.commit()
		msg = "task updated"
	except:
		conn.rollback()
		msg = "error in update operation"
	finally:		
		return (msg)
		conn.close()

#######################################################################
@app.route("/removetask",methods=['POST'])
def removetask():
	try:
		taskid = request.form['taskid']
		conn = sqlite3.connect("todolist.db")
		cur = conn.cursor()
		cur.execute("insert into deletedtasks select * from list where id = ?",(taskid,))
		cur.execute("delete from list where id = ?",(taskid,))

		conn.commit()
		msg = "task deleted"
	except:
		conn.rollback()
		msg = "error in delete operation"
	finally:	
		return (msg)
		conn.close()
#######################################################################
@app.route("/finishtask",methods=['POST'])
def finishtask():
	try:
		taskid = request.form['taskid']
		conn = sqlite3.connect("todolist.db")
		cur = conn.cursor()
		cur.execute("insert into completedtasks select * from list where id = ?",(taskid,))
		cur.execute("delete from list where id = ?",(taskid,))

		conn.commit()
		msg = "task completed"
	except:
		conn.rollback()
		msg = "error in delete operation"
	finally:	
		return (msg)
		conn.close()
######################################################################
@app.route("/signedin")
def signedin():
	if (loggedin_username):
		return render_template("signedin.html",loggedin_username=loggedin_username)
	else:
		return render_template("index.html")
#######################################################################
@app.route("/signout")
def signout():
	global loggedin_email
	global loggedin_username
	loggedin_email = ''
	loggedin_username = ''
	return render_template("index.html")
#######################################################################
if __name__ == "__main__ ":
	app.run(debug=True)


########################################################################
