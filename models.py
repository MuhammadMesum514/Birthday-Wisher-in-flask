# from flask import Flask,render_template
# from flask_sqlalchemy import SQLAlchemy
# import app
import os
from dotenv import load_dotenv
load_dotenv()
name=os.getenv("DEFAULT_EMAIL")
print(name)
# import datetime
# app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# db = SQLAlchemy(app)

# class Members(db.Model):
#     id = db.Column(db.Integer, primary_key=True, )
#     name = db.Column(db.String(30) )
#     email = db.Column(db.String(80))
#     dob = db.Column(db.Date)

#     def __init__(self,name,email,dob):
#         self.name=name
#         self.email=email
#         self.dob=do
       

#     def __repr__(self)->str:
#         return self.id

