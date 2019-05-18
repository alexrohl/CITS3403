from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Results, Polls

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class VoteForm(FlaskForm):
    radio_button1 = RadioField('Default', choices=[(1,'Farruh'),(2,'is')])
    radio_button2 = RadioField('Default', choices=[(1,'a'),(2,'dickhead')])
    radio_button3 = RadioField('Default', choices=[(1,'lets'),(2,'see')])
    radio_button4 = RadioField('Default', choices=[(1,'if'),(2,'he')])
    radio_button5 = RadioField('Default', choices=[(1,'even'),(2,'notices')])
    radio_button6 = RadioField('Default', choices=[(1,'this'),(2,'omg')])
    radio_button7 = RadioField('Default', choices=[(1,'what'),(2,'a')])
    radio_button8 = RadioField('Default', choices=[(1,'spud'),(2,'just')])

    submit = SubmitField('Vote!')


class CreatePollForm(FlaskForm):
    metric = StringField('Metric', validators=[DataRequired()])
    submit = SubmitField('Submit New Poll')

class DeletePollForm(FlaskForm):
    radio_button = RadioField('Select Metric', choices=[(1,'Farruh'),(2,'is')])
    submit = SubmitField('Delete!')

class CreateCharacterForm(FlaskForm):
    character = StringField('Character', validators=[DataRequired()])
    submit = SubmitField('Submit New Character')

class DeleteCharacterForm(FlaskForm):
    radio_button = RadioField('Select Character', choices=[(1,'Farruh'),(2,'is')])
    submit = SubmitField('Delete')
