from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, ValidationError
from application.models import User

class PostForm(FlaskForm):
    title = StringField('Rubrik', validators=[DataRequired()])
    content = TextAreaField('Brödtext', validators=[DataRequired()])
    picture = FileField('Ladda upp bild', validators=[FileAllowed(['jpg','png'])])
    youtube = StringField('youtube-länk')
    submit = SubmitField('Publicera')
    def validate_youtube(self, youtube):
        if youtube.data != "":
            if not  "youtube.com" in youtube.data:
                raise ValidationError("Länken måste vara en youtube länk")

class NewReply(FlaskForm):
    message = TextAreaField()
    submitreply = SubmitField('kommentera')

class EventForm(FlaskForm):
    title = StringField('Rubrik', validators=[DataRequired()])
    content = TextAreaField('Brödtext', validators=[DataRequired()])
    youtube = StringField('YouTube-länk')
    picture = FileField('Bild', validators=[FileAllowed(['jpg','png'])])
    location = StringField('Plats')
    event_date = DateField('Eventet äger rum', format='%d-%m-%Y')  
    time = StringField('Klockan mm:hh')
    last_registration = DateField('Sista anmälan', format='%d-%m-%Y')   
    max_participants = IntegerField('Antal platser')
    submit = SubmitField('Publicera')  

class AttendingEventForm(FlaskForm):
    number = IntegerField('Ett nummer')
    submitattending = SubmitField('Anmäl dig')

