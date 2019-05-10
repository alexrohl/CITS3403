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

class VotingForm(FlaskForm):
    metric = StringField('Metric', validators=[DataRequired()])
    alpha_character = StringField('Alpha Character', validators=[DataRequired()])
    beta_character = StringField('Beta Character', validators=[DataRequired()])
    radio_button = RadioField('Label', choices=[('value','description'),('value_two','whatever')])
    submit = SubmitField('Vote!')

    def add_button(self, char1, char2, metric):
        setattr(self, metric, RadioField('Label', choices=[(1,char1),(2,char2)]))



class VoteForm(FlaskForm):
    radio_button = RadioField('Label', choices=[(1,'Iron Man'),(2,'Thor')])


class CreatePollForm(FlaskForm):
    metric = StringField('Metric', validators=[DataRequired()])
    submit = SubmitField('Submit Poll')
