import os
import secrets
import json
from datetime import datetime, timedelta

from application import app, bcrypt, db
from application.models import AttendingEvent, Event, Post, User, User_info
from application.users.forms import (LoginForm, RegistrationForm,
                                     UpdateAccountForm)
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

users = Blueprint('user', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('posts.home'))

    return render_template('login.html', form=form)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        user_id = User.query.filter_by(email=form.email.data).first()
        user_info = User_info(user_id=user.id, food_preference=form.food_preference.data, semester=form.semester.data, gender=form.gender.data)
        db.session.add(user_info)
        db.session.commit()
        
        return redirect(url_for('user.login'))  
    return render_template('register.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) 

    return picture_fn

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    user_info = User_info.query.filter_by(id=current_user.id).first()
    password = User.query.filter_by(password=current_user.password).first()
    attended_events = event_id = AttendingEvent.query.join(Event).filter(AttendingEvent.user_id==current_user.id ,Event.event_date < datetime.today()).order_by(Event.event_date).all()
    #User does not change password
    if form.validate_on_submit() and form.new_password.data == "":
        flash(f'Ditt konto är nu uppdaterat!', 'success')        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        user_info.food_preference = form.food_preference.data
        user_info.semester = form.semester.data
        db.session.commit()
    #User change password
    elif form.validate_on_submit() and form.old_password.data != "":
        if bcrypt.check_password_hash(current_user.password,form.old_password.data): 
            flash(f'Ditt konto och lösenord är nu uppdaterat!', 'success')        
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            hashed_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('utf-8')
            current_user.email = form.email.data
            user_info.food_preference = form.food_preference.data
            user_info.semester = form.semester.data
            current_user.password = hashed_password
            db.session.commit()

    elif form.validate_on_submit():
        flash(f'Någonting gick snett, försök igen!', 'danger')    

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.food_preference.data = user_info.food_preference
        form.semester.data = user_info.semester

    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    return render_template('account.html', image_file=image_file, form=form, user_info=user_info, attended_events=attended_events, user_warning=user_warning)

@users.route('/booking', methods=['GET','POST'])
@login_required
def booking():
    page = request.args.get('page',1, type=int)

    d = datetime.today() - timedelta(days=1)
    bookings = Post.query.join(Event, AttendingEvent).filter(Post.event_id==Event.id==AttendingEvent.event_id, AttendingEvent.user_id==current_user.id, Event.event_date > d).order_by(Event.event_date).paginate(page=page, per_page=8)
    #event_id = AttendingEvent.query.join(Event).filter(AttendingEvent.user_id==current_user.id ,Event.event_date > d).order_by(Event.event_date).paginate(page=page, per_page=8)
    user_info = User_info.query.filter_by(user_id=current_user.id).first()
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    

    return render_template('booking.html', event_id=bookings, user_info=user_info, user_warning=user_warning)

@users.route('/dashboard', methods=['GET','POST'])
def dashboard():
    user_info = User_info.query.filter_by(id=current_user.id).first()
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    #Data to genderfields
    #Getting data
    num_total = []
    num_male = []
    num_female = [] 
    hosted_events = Post.query.filter_by(author=current_user).filter(Post.event_id != None).all()
    num_events = len(hosted_events)
    for event in hosted_events:
        attending = AttendingEvent.query.filter_by(event_id=event.event_id).all()
        for student in attending:
            print(student.gender)
            if student.gender == "male":
                num_male.append(1)
            else:
                num_female.append(1)
    num_male = int(len(num_male))
    num_female = int(len(num_female))
    num_tot = num_male + num_female
    #Percentages
    if num_tot==0:
        num_tot=1
    percentage_male= num_male/(num_tot)
    percentage_female= num_female/(num_tot)
    percentage_male = "{:.0%}".format(percentage_male)
    percentage_female = "{:.0%}".format(percentage_female)
    
    #Sending data to graph
    date = []
    attending = []
    historical_events = {}
    for event in Event.query.all():
        date.append(event.event_date.isoformat())
        attending.append(len(AttendingEvent.query.filter_by(event_id=event.id).all()))
    data= ""
    for k,v in zip(date,attending):
        data +="{t: '"+k+"',y: " +str(v)+"},"
 
    #circle-diagram
    semester_total = len(AttendingEvent.query.all())
    # GÖRA färdigt: semester1 = len(AttendingEvent.query.filter_by(semester=1))
   
    return render_template('dashboard.html', user_info=user_info,  attending=attending,data=data, num_events=num_events, num_tot=num_tot, percentage_female=percentage_female, percentage_male=percentage_male, user_warning=user_warning )

@users.route('/calendar/event', methods=['GET','POST'])
def calendar_event():
    user_info = User_info.query.filter_by(id=current_user.id).first()
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    
    return render_template('fullcalendar.html', user_info=user_info,  user_warning=user_warning )

@users.route('/quotes', methods=['GET','POST'])
def qutoes():
    user_info = User_info.query.filter_by(id=current_user.id).first()
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    
    return render_template('quotes.html', user_info=user_info,  user_warning=user_warning )


## admin
admin = Admin(app, template_mode='bootstrap3')

admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(AttendingEvent, db.session))
admin.add_view(ModelView(User_info, db.session))
