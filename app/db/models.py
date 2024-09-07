from app import app

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
from datetime import datetime


db=SQLAlchemy(app)



class BlogPost(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    title=db.Column(db.String(200))
    subtitle=db.Column(db.String(200))
    date_created=db.Column(db.DateTime, default=datetime.now())
    content=db.Column(db.Text)



class AnalysisReport(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    number_of_reports=db.Column(db.Integer,default=1)
    match_id=db.Column(db.Integer,unique=True)



class MatchAnalysis(db.Model):
    created_by=db.Column(db.Integer,nullable=True)
    match_id=db.Column(db.Integer, primary_key=True,unique=True)
    match_analysis_content=db.Column(db.Text,unique=True)
    date_created=db.Column(db.DateTime, default=datetime.now(),nullable=True)

class MOTD(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    date=db.Column(db.DateTime,default=datetime.now(),unique=True)
    content=db.Column(db.Text)
    
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip=db.Column(db.String(15),nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.now())
    sub_expire=db.Column(db.DateTime, default=datetime.now())
    sub_type=db.Column(db.Integer,default=0,nullable=True)
    signup_date = db.Column(db.DateTime, default=datetime.now())
    signup_ref=db.Column(db.String(12),default="1",nullable=True)
    ref_code=db.Column(db.String(12), default=''.join(random.choices(string.ascii_letters + string.digits, k=12)))
    refs=db.Column(db.Integer,default=0)
    admin=db.Column(db.Boolean,nullable=True)
    
class Subs_Bought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date=db.Column(db.DateTime, default=datetime.now())
    user_id=db.Column(db.Integer,nullable=False)
    sub_type=db.Column(db.Integer,nullable=False)
    
    
class ProfileBet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id=db.Column(db.Integer,unique=False)
    user_id=db.Column(db.Integer, unique=False)
