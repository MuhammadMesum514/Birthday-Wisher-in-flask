from flask import Flask, render_template,request,redirect,session
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from dotenv import load_dotenv
from sqlalchemy.orm import load_only
from flask_session import Session
load_dotenv()
# app and db cofiguration
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
# configuring session
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

is_login=False #check login status
#handle error route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
app.register_error_handler(404, page_not_found)

# set configuration and instantiate mail
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}
app.config.update(mail_settings)
mail = Mail(app)

                # database table for login
class Login(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(30))

    def __init__(self,username,passoword):
        self.username=username
        self.password=passoword

    def __repr__(self)->str:
        return "(%r, %r, %r)" %(self.uid, self.username, self.password)
    

            #""" database table for storing birthday"""

class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30) )
    email = db.Column(db.String(80))
    dob = db.Column(db.Date)

    def __init__(self,name,email,dob):
        self.name=name
        self.email=email
        self.dob=dob
       
    def __repr__(self)->str:
        return "(%r, %r, %r)" %(self.id, self.name, self.email)

        #""" routing for pages """

#  main page  
@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")    
    else:
        AllRecords= Members.query.all();
        return render_template("main.html",records=AllRecords)

@app.route("/login", methods=['GET', 'POST'])
# @app.route("/index", methods=['GET', 'POST'])
# @app.route("/login", methods=['GET', 'POST'])
def login():
    global is_login
    if request.method == 'POST':      
        username=request.form.get("username")
        password=request.form.get("password")
        if (username==os.environ['LOGIN_USERNAME'] and password==os.environ['LOGIN_PASSWORD']):
            session['name']=username
            return redirect("/")
    else:
          return render_template("login.html")

# navigate to add a bday record
@app.route("/Add_Birthday")
def AddNewBirthday():
   return render_template("Add_Birthday.html")
    

# ADDING A BIRTHDAY RECORD
@app.route("/greet", methods=["POST"])
def greet():
   
    name=request.form.get("name")
    email=str(request.form.get("email"))
    bday=request.form.get("birthday")
    bday_formatted=datetime.strptime(bday,"%Y-%m-%d").date()  
    users= Members(name=name,email=email,dob=bday_formatted)
    db.session.add(users)
    db.session.commit()
    return render_template("Add_Birthday.html")
    

    
# DELETING A BIRTHDAY RECORD
@app.route("/delete/<int:id>")
def delete(id):
    Members.query.filter_by(id=id).delete()
    # db.session.delete(toDelete)
    db.session.commit()
    return redirect("/")

# WISHING THE BIRTHDYA
@app.route("/wish/<int:id>")
def wish(id):
    
    # getting user infro
    reciever_name=Members.query.with_entities(Members.name).filter_by(id=id).first()
    reciever_name=''.join(reciever_name) #convert tuple into string 
    greeting_message=f"Happy Birthday {reciever_name} \n many manay Happy Returns of the Day. May you Have all the Blessings of Life. Enjoy YOur Day and Party Hard.\n Hope you have a Great Day \n Regards: Muhammad Mesum"
    recieving_address=Members.query.with_entities(Members.email).filter_by(id=id).first()
    mail_reciver=''.join(recieving_address) 
   
    # sending the mail
    msg = Message(subject="BIRTHDAY WISH",
         sender=app.config.get("MAIL_USERNAME"),
          recipients=[mail_reciver], # replace with your email for testing
          body=greeting_message)
    mail.send(msg)   
    return redirect("/index")
    
@app.route("/logout")
def logout():
    session["name"]=None
    return redirect("/login")   


@app.context_processor
def inject_now():
    return {'now': datetime.now()}

if __name__=="main":
    app.run(debug=True)
