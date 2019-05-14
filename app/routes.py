from os import getenv
from flask import render_template, flash, redirect, url_for, request, Blueprint, request, jsonify, session
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreatePollForm, DeletePollForm, CreateCharacterForm, DeleteCharacterForm, VoteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Results, Polls, Votes, Characters
from werkzeug.urls import url_parse
import itertools
import random

@app.route('/')
@app.route('/index')
@login_required
def index():
    recent_votes = [vote.to_json() for vote in Votes.query.all()][-5:]
    users = [user.to_json() for user in User.query.all()]
    #make a function to match stuff..?
    for vote in recent_votes:
        for user in users:
            if vote['user_id'] == user['id']:
                vote['user_id'] = user['username']
                break
    return render_template('index.html', title='Home Page', results=recent_votes)

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
        print(user)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/results', methods=['GET','POST'])
def results():
    results = [vote.to_json() for vote in Votes.query.all()]
    return render_template('results.html', title='Results Page', results = results)

# retrieves/adds polls from/to the database
@app.route('/admin_options', methods=['GET', 'POST'])
def admin_options():
    metrics = [poll.metric for poll in Polls.query.all()]
    characters = [character.character for character in Characters.query.all()]


    form1 = CreatePollForm()
    form2 = DeletePollForm()
    choices = [(x,x) for x in metrics]
    form2.radio_button.choices = choices
    form3 = CreateCharacterForm()
    form4 = DeleteCharacterForm()

    #let admins create new metrics to be voted on
    if form1.validate_on_submit():
        poll = Polls(user_id=current_user.username,
                     metric=form1.metric.data)
        db.session.add(poll)
        db.session.commit()
        flash('Poll created!')

    #let admins delete metrics
    elif form2.validate_on_submit():
        return

    #let admins create new characters to be voted

    elif form3.validate_on_submit():
        new_character = Characters(user_id=current_user.username,
                     character=form3.character.data)
        db.session.add(new_character)
        db.session.commit()
        flash('Character added!')

    #let admins delete metrics

    return render_template('admin_options.html', form1=form1, form2=form2, form3=form3, form4=form4, metrics=metrics, characters=characters)



'''BELOW IS ALL THE VOTING METHODS FOR vote.html. THERES A LOT OF CODE BECAUSE IT WAS TOO TEDIOUS TO
CREATE THE FORMS DYNAMICALLY FOR ALL THE DATA '''

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    metrics = [poll.metric for poll in Polls.query.all()]
    characters = [character.character for character in Characters.query.all()]
    characters = list(itertools.combinations(characters,2))
    print('CHARACTERS',characters)
    print('METRICS',metrics)
    form = VoteForm()

    #GENERATES random selection of 10 metrics/character pairs
    num_metrics = len(metrics)
    num_characters = len(characters)
    random_pairs = random.sample(range(num_characters),2)*5
    random_metrics = [0] + random.sample(range(num_metrics),3)*3

    #MAJOR issues creating forms dynamically so have to do it old school
    form.radio_button1.label.text = metrics[random_metrics[0]]
    form.radio_button1.choices = [(1,characters[random_pairs[0]][0]),(2,characters[random_pairs[0]][1])]
    form.radio_button2.label.text = metrics[random_metrics[1]]
    form.radio_button2.choices = [(1,characters[random_pairs[1]][0]),(2,characters[random_pairs[1]][1])]
    form.radio_button3.label.text = metrics[random_metrics[2]]
    form.radio_button3.choices = [(1,characters[random_pairs[2]][0]),(2,characters[random_pairs[2]][1])]
    form.radio_button4.label.text = metrics[random_metrics[3]]
    form.radio_button4.choices = [(1,characters[random_pairs[3]][0]),(2,characters[random_pairs[3]][1])]
    form.radio_button5.label.text = metrics[random_metrics[4]]
    form.radio_button5.choices = [(1,characters[random_pairs[4]][0]),(2,characters[random_pairs[4]][1])]
    form.radio_button6.label.text = metrics[random_metrics[5]]
    form.radio_button6.choices = [(1,characters[random_pairs[5]][0]),(2,characters[random_pairs[5]][1])]
    form.radio_button7.label.text = metrics[random_metrics[6]]
    form.radio_button7.choices = [(1,characters[random_pairs[6]][0]),(2,characters[random_pairs[6]][1])]
    form.radio_button8.label.text = metrics[random_metrics[7]]
    form.radio_button8.choices = [(1,characters[random_pairs[7]][0]),(2,characters[random_pairs[7]][1])]
    form.radio_button9.label.text = metrics[random_metrics[8]]
    form.radio_button9.choices = [(1,characters[random_pairs[8]][0]),(2,characters[random_pairs[8]][1])]
    form.radio_button10.label.text = metrics[random_metrics[9]]
    form.radio_button10.choices = [(1,characters[random_pairs[9]][0]),(2,characters[random_pairs[9]][1])]

    #AGAIN MAJOR issues submitting forms dynamically so doing it for fixed amounts of votes.
    if form.is_submitted():
        first_char = form.radio_button1.choices[0][1]
        second_char = form.radio_button1.choices[1][1]
        if int(form.radio_button1.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button1.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button1.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button1.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('fail')

        first_char = form.radio_button2.choices[0][1]
        second_char = form.radio_button2.choices[1][1]
        if int(form.radio_button2.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button2.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button2.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button2.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('fail')

        first_char = form.radio_button3.choices[0][1]
        second_char = form.radio_button3.choices[1][1]
        if int(form.radio_button3.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button3.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button3.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button3.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('fail')

        first_char = form.radio_button4.choices[0][1]
        second_char = form.radio_button4.choices[1][1]
        if int(form.radio_button4.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button4.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button4.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button4.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('fail')

        first_char = form.radio_button5.choices[0][1]
        second_char = form.radio_button5.choices[1][1]
        if int(form.radio_button5.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button5.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button5.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button5.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('button 5 fail')

        first_char = form.radio_button6.choices[0][1]
        second_char = form.radio_button6.choices[1][1]
        if int(form.radio_button6.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button6.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button6.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button6.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('button 6 fail')

        first_char = form.radio_button7.choices[0][1]
        second_char = form.radio_button7.choices[1][1]
        if int(form.radio_button7.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button7.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button7.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button7.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('button 7 fail')

        first_char = form.radio_button8.choices[0][1]
        second_char = form.radio_button8.choices[1][1]
        if int(form.radio_button8.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button8.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button8.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button8.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('button 8 fail')

        first_char = form.radio_button9.choices[0][1]
        second_char = form.radio_button9.choices[1][1]
        if int(form.radio_button9.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button9.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button9.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button9.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('button 9 fail')

        first_char = form.radio_button10.choices[0][1]
        second_char = form.radio_button10.choices[1][1]
        if int(form.radio_button10.data) == 1:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=first_char,
                             beta_character=second_char,
                             metric=form.radio_button10.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
            flash('Vote submitted!')
        elif int(form.radio_button10.data) == 2:
            new_vote = Votes(
                             user_id=current_user.id,
                             alpha_character=second_char,
                             beta_character=first_char,
                             metric=form.radio_button10.label.text
                             )
            db.session.add(new_vote)
            db.session.commit()
        else:
            print('button 10 fail')

    else:
        print('fail')
        print(form.errors)

    return render_template('vote.html', title='Vote', form=form, metrics=metrics, characters=characters)

            #might need to indent this
