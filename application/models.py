from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from application import db, login_manager
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    image_file = db.Column(db.String(), default='default.jpg')

    #Relationships
    user_info = db.relationship('User_info', backref='info')
    posts = db.relationship('Post', backref='author', lazy=True)
    attenindingevent = db.relationship('AttendingEvent', backref='user', lazy=True)
    replies = db.relationship('Reply', backref='user', lazy='dynamic')
    def __repr__(self):
        return (self.username)
    

class User_info(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_type = db.Column(db.String(), unique=False, default="student")
    food_preference = db.Column(db.String(), unique=False, default=None)
    gender = db.Column(db.String(), unique=False, default=None)
    warnings = db.Column(db.Integer(), unique=False, default=0)
    semester = db.Column(db.Integer(), unique=False, nullable=False)
    def __repr__(self):
        return (self.food_preference)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=True, default=None)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    image_file = db.Column(db.String(), unique=False, default=None)
    youtube = db.Column(db.String(), nullable=True, default=None)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    def __repr__(self):
        return (self.title)
    
    #relationships
    replies = db.relationship('Reply', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)
    get_event = db.relationship('Event', backref='post', lazy=True)
    

class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    event_name = db.Column(db.String())
    location = db.Column(db.String(), nullable=True, unique=False)
    event_date = db.Column(db.DateTime(), nullable=True, default=datetime.utcnow)
    event_time = db.Column(db.String(), nullable=True) 
    last_registration = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    max_participants = db.Column(db.Integer,unique=False, default=0)
    posts = db.relationship('Post', backref='event', lazy=True)
    attending = db.relationship('AttendingEvent', backref='event', lazy=True)
    def __repr__(self):
        return (self.event_name)


class AttendingEvent(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gender = db.Column(db.String)
    present = db.Column(db.String, default="notpresent")
    warning = db.Column(db.String, default="nowarning")
    register_time = db.Column(db.DateTime(), nullable=True, default=datetime.utcnow)
    attendingevent = db.relationship('Event', backref='attendingevent', lazy=True)
    
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id')) 
    liked_post = db.relationship('Post', backref='liked_post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime())

class Quotes(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    quote = db.Column(db.String())
    name = db.Column(db.String(), nullable=True, unique=False)
    def __repr__(self):
        return (self.event_name)
