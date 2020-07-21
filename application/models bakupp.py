from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from application import db, login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##################

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=False, Nullabe=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    image_file = db.Column(db.String(), default='default.jpg')

    #Relationships
    user_info = db.relationship('User_info', backref='user_id')
    author = db.relationshop('Post', backref='author')

class User_info(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_type = db.Column(db.String(), unique=False, default="student")
    food_preference = db.Column(db.String(), unique=False, default=None)
    warnings = db.Column(db.Integer(), unique=False, default=0)
    semester = db.Column(db.Integer(), unique=False, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.string(), nullable=True, default=None)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    image_file = db.Column(db.String(), unique=False, default=None)

class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event_id = db.Integer(db.ForeingKey('post.id'))
    event_name = db.String(db.ForeingKey('post.title'))
    location = db.Column(db.String(), nullable=True, unique=False)
    event_date = db.Column(db.String(), nullable=True)
    event_time = db.Column(db.String(), nullable=True)
    last_registration = db.Column(db.String, nullable=False)
    max_participants = db.Column(db.Integer,unique=false, default=0)

efault=datetime.utcnow)

#####################

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    food_preference = db.Column(db.String(), unique=False, nullable=False, default="")
    warnings = db.Column(db.String(), unique=False, nullable=False, default=0)
    semester = db.Column(db.Integer(), unique=False, default=0)
    
    #Relationships
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f"User('self.username', 'self.email')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default="none")
    
    #Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.relationship('Event', backref="post", lazy=True)
    def __repr__(self):
        return f"Post('self.title', 'self.date_posted')"
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Integer, db.ForeignKey('post.id'))
    max_participants = db.Column(db.Integer, unique=False, default=0)
    last_registration = db.Column(db.String, nullable=False)
    event_date= db.Column(db.String, nullable=False)
    user_registration_time=  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    #Relationship






