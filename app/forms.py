from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Results

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

class VotingForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    metric = StringField('Metric', validators=[DataRequired()])
    character_alpha = StringField('Alpha Character', validators=[DataRequired()])
    character_beta = StringField('Beta Character', validators=[DataRequired()])
    submit = SubmitField('Vote!')

class CreatePollForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    metric = StringField('Metric', validators=[DataRequired()])
    submit = SubmitField('Submit Poll')
