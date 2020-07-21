from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Juridiskt kön', choices =[('male','man'),('female','kvinna')])
    password = PasswordField('Password', validators= [DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    food_preference = StringField('Allergi, matpreferenser')
    semester = IntegerField('Årskurs', validators=[DataRequired()])
    submit = SubmitField('Registrera')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Denna emailen är redan registrerad')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    food_preference = StringField('Allergi, matpreferenser')
    semester = IntegerField('Årskurs', validators=[DataRequired()])
    submit = SubmitField('Uppdatera')
    picture = FileField('Uppdatera profilbild', validators=[FileAllowed(['jpg','png'])])
    old_password = PasswordField('Befintligt lösenord', default=None)
    new_password = PasswordField('nytt lösenord', default=None)
    confirm_password = PasswordField('bekräfta nytt lösenord', validators=[ EqualTo('new_password')],default=None) 
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Denna emailen är redan registrerad')
    def validate_password(self,old_password):
        password = User.query.filter_by(password=form.old_password.data).first()
        if not( password and bcrypt.check_password_hash(user.password,form.old_password.data)):
            raise ValidationError('Fel lösenord')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('logga in')