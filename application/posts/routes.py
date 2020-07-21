from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify, request
import secrets
from PIL import Image
import os
from flask_login import login_required, current_user
from application import app, db
from application.posts.forms import PostForm, EventForm, AttendingEventForm, NewReply
from application.models import Post, User, Event, User_info, AttendingEvent, Reply, Like
from datetime import datetime, timedelta
from random import randint

posts = Blueprint('posts', __name__)


#Functions

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

#main

@posts.route('/homepage', methods=['GET','POST'])
@posts.route('/', methods=['GET','POST'])
@posts.route('/home', methods=['GET','POST'])
@login_required
def home():
    page = request.args.get('page',1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
    user_info = User_info.query.filter_by(id=current_user.id).first()
    #User warnings
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    return render_template('homepage.html', posts=posts, current_user=current_user, user_info=user_info, user_warning=user_warning)


@posts.route('/post/<int:post_id>', methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form1 = AttendingEventForm()
    form2 = NewReply()
    event_id= post.event_id
    state = None
    like_status = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
    
    if like_status:
        like_status="active"
    if event_id:
       last_registration = Event.query.get_or_404(event_id).last_registration
    attending = AttendingEvent.query.filter_by(event_id=event_id).filter_by(user_id=current_user.id).first()
    
    #Register button
    if event_id:
        if not attending:
            if datetime.now() - timedelta(days=1) < last_registration :
                state = "notattendning"
        if attending:
            if datetime.now() - timedelta(days=1) < last_registration :
                state = "attending"
        if datetime.now() - timedelta(days=1) > last_registration :
            state = "closed"
        
        if ("register" in request.form and form1.validate_on_submit()) and not attending and (len(post.event.attendingevent) < post.event.max_participants or post.event.max_participants == 0):   
            attending = AttendingEvent(event_id=event_id, user_id=current_user.id, gender=User_info.query.filter_by(id=current_user.id).first().gender)
            db.session.add(attending)
            db.session.commit()
            flash(f'Du är nu anmäld!', 'success')   
            return redirect(url_for('posts.like_post', post_id=post.id))
        if not (datetime.now() - timedelta(days=1) > last_registration) and ("register" in request.form and form1.validate_on_submit()):
            flash(f'Du är nu avanmäld!', 'success')   
            
            db.session.delete(attending)
            db.session.commit()
            return redirect(url_for('posts.like_post', post_id=post.id))
    
            
    #comments
    replies = Reply.query.filter_by(post_id=post_id).all()
    print(replies)
    
        
    if ("comment" in request.form and form2.validate_on_submit()) and form2.message.data:
        comment = Reply(post_id=post.id, user_id=current_user.id, message=form2.message.data)
        db.session.add(comment)
        db.session.commit()
        flash(f'Du har kommenterat!', 'success') 

    elif form2.validate_on_submit():
        flash(f'Någonting gick snett, försök igen!', 'danger') 
    
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)

    return render_template('post.html', current_user=current_user, post=post, form=form1, form_reply=form2, replies=replies, state=state, like_status = like_status, user_info = User_info.query.filter_by(id=current_user.id).first(), user_warning=user_warning)

@posts.route("/user/<int:id>")
@login_required
def user_posts(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    return render_template('user_posts.html', posts=posts, user=user, user_info = User_info.query.filter_by(id=current_user.id).first(), user_warning=user_warning)


#Creating/updating posts/events
@posts.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        url = form.youtube.data.replace("watch?v=", "embed/")
        if form.youtube.data == "":
            url = None           
        if form.picture.data:
            image_file = save_picture(form.picture.data)
        if not form.picture.data:
            image_file = ""
        
        post = Post(title=form.title.data, content=form.content.data, youtube=url, author=current_user, image_file=image_file)
        db.session.add(post)
        db.session.commit()
    

        return redirect(url_for('posts.home'))
    user_info = User_info.query.filter_by(id=current_user.id).first()
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    return render_template('create_post.html', form=form, user_info = user_info, user_warning=user_warning)

@posts.route('/post/new/event', methods=['GET','POST'])
@login_required
def new_event():
    form = EventForm()  
    if form.validate_on_submit():
        print(form.youtube.data)
        url = form.youtube.data.replace("watch?v=", "embed/")
        if form.youtube.data == "":
            url = None           
        if form.picture.data:
            image_file = save_picture(form.picture.data)
        if not form.picture.data:
            image_file = ""
        event = Event( event_name=form.title.data, event_time=form.time.data, location=form.location.data, event_date=form.event_date.data, last_registration=form.last_registration.data, max_participants=form.max_participants.data)
        db.session.add(event)
        db.session.flush()
        post = Post(title=form.title.data, content=form.content.data, youtube=url, author=current_user, image_file=image_file, event_id=event.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.home'))
    user_info = User_info.query.filter_by(id=current_user.id).first()
    return render_template('new_event.html', form=form, user_info=user_info)

@posts.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_info = User_info.query.filter_by(user_id=current_user.id).first()
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, user_info=user_info, user_warning=user_warning)

@posts.route('/post/<int:post_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.home'))

@posts.route('/post/event/<int:post_id>', methods=['GET','POST'])
@login_required
def table(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        event_id = Post.query.filter_by(id=post_id).first().event_id
        table = AttendingEvent.query.filter_by(event_id=event_id).join(User_info, User_info.user_id == AttendingEvent.user_id).all()
        allergies = AttendingEvent.query.filter_by(event_id=event_id).join(User_info, User_info.user_id == AttendingEvent.user_id).all()
        user_info = User_info.query.filter_by(id=current_user.id).first()
        get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
        user_warning = []
        for warning in get_warnings:
            event = Post.query.filter(Post.event_id==warning.event_id).first()
            user_warning.append(event)
        
        return( render_template('table.html', table=table, current_user=current_user, user_info=user_info, event_id=event_id, user_warning=user_warning))

@posts.route('/post/event/update', methods=['POST', 'GET'])
def update_attending():
    user = User.query.filter_by(id=request.form['id']).first()
    event_id = AttendingEvent.query.filter_by(event_id=request.form['event_id'], user_id = user.id).first()
    db.session.commit()
    if event_id.present == "notpresent":
        event_id.present = "present"
        db.session.commit()
            
    elif event_id.present == "present":
        event_id.present = "notpresent"
        db.session.commit()
        
    
    
    
    return jsonify({'result' : 'success', 'username' : user.username, 'present' : event_id.present})

@posts.route('/post/event/warning', methods=['POST', 'GET'])
def update_warning():
    user = User.query.filter_by(id=request.form['id']).first()
    user_info = User_info.query.filter_by(user_id=request.form['id']).first()
    event_id = AttendingEvent.query.filter_by(event_id=request.form['event_id']).first()
    db.session.commit()
    if event_id.warning == "nowarning":
        event_id.warning = "warning"
        user_info.warnings += 1 
        db.session.commit()
        print("1")     
    elif event_id.warning == "warning":
        event_id.warning = "nowarning"
        user_info.warnings -= 1 
        db.session.commit()
        print("2")
    
    
    
    
    return jsonify({'result' : 'success', 'username' : user.username, 'warning' : event_id.warning})


@posts.route('/post/<int:post_id>/like', methods=['GET','POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    is_liked = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
    like  = Like(user_id=current_user.id, post_id=post_id)
    if not is_liked:
        db.session.add(like)
        db.session.commit()
    else:
        db.session.delete(is_liked)
        db.session.commit()

    return redirect(url_for('posts.post', post_id=post.id))


@posts.route('/upcomingevents', methods=['GET','POST'])
@login_required
def upcoming_events():
    page = request.args.get('page',1, type=int)
    event_id = Post.query.join(Event).filter(Post.event_id==Event.id, Event.event_date > datetime.now() - timedelta(days=1)).order_by(Event.event_date).paginate(page=page, per_page=8)
    user_info = User_info.query.filter_by(id=current_user.id).first()
    get_warnings = AttendingEvent.query.filter(AttendingEvent.warning=='warning').filter(AttendingEvent.user_id==current_user.id).all()
    user_warning = []
    for warning in get_warnings:
        event = Post.query.filter(Post.event_id==warning.event_id).first()
        user_warning.append(event)
    

    return render_template('upcoming_events.html', event_id=event_id, user_info=user_info, user_warning=user_warning)
