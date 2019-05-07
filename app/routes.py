from os import getenv
from flask import render_template, flash, redirect, url_for, request, Blueprint, request, jsonify, session
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreatePollForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Results, Polls
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Zenn'}
    posts = [
        {
            'author': {'username': 'Lachie'},
            'body': 'Flexin everyday'
        },
        {
            'author': {'username': 'Zenn'},
            'body': 'Spinning rainbow squares!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/results', methods=['GET','POST'])
def results():
    results = [
        {
            'character': 'Iron Man',
            'metric': 'Strength',
            'score': 1000
        },
        {
            'character': 'Iron Man',
            'metric': 'Speed',
            'score': 1200
        },
        {
            'character': 'Thor',
            'metric': 'Strength',
            'score': 2000
        }
    ]
    return render_template('results.html', title='Results Page', results = results)

# retrieves/adds polls from/to the database
@app.route('/createpoll', methods=['GET', 'POST'])
def createpoll():
    form = CreatePollForm()
    if form.validate_on_submit():
        poll = Polls(user_id=user.username,
                     metric=form.metric.data)
        db.session.add(poll)
        db.session.commit()
        flash('Poll created!')

    return render_template('createpoll.html', title='Polls', form=form)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    form = VotingForm()
    if form.validate_on_submit():
        vote = Votes(user_id=user.username,
                     metric=form.metric.data,
                     alpha_character = form.alpha_character.data,
                     beta_character = form.beta_character.data)
        db.session.add(vote)
        db.session.commit()
        flash('Vote submitted!')

    return render_template('vote.html', title='Vote', form=form)
'''
