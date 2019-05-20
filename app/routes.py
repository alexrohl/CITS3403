from os import getenv
from flask import render_template, flash, redirect, url_for, request, Blueprint, request, jsonify, session
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreatePollForm, DeletePollForm, CreateCharacterForm, DeleteCharacterForm, VoteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Results, Polls, Votes, Characters
from werkzeug.urls import url_parse
import itertools
import random
import math

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


def initialise_Results_Table(characters, metrics):
    results = Results.query.all()
    print(results)
    for r in results:
        db.session.delete(r)
    print("results table cleaned")
    for metric in metrics:
        for character in characters:
            new_result = Results(character=character, metric=metric, score = 1000)
            print(new_result)
            db.session.add(new_result)
            db.session.commit()
    print([result for result in Results.query.all()])
    return

def Probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

#updates the Results table for each sequential vote
def update_Results_table(results_rows,beta_character,alpha_character,metric):
    K=30 #elo ranking constant
    for row_alpha in results_rows:
        if row_alpha.metric == metric and row_alpha.character == alpha_character:
            alpha_score = row_alpha.score
            break
    for row_beta in results_rows:
        if row_beta.metric == metric and row_beta.character == beta_character:
            beta_score = row_beta.score
            break
    P_alpha = Probability(alpha_score, beta_score)
    P_beta = Probability(beta_score, alpha_score)
    new_alpha_score = alpha_score + K * (1-P_alpha)
    new_beta_score = beta_score + K * (0-P_beta)
    #update scores
    row_alpha.score = int(new_alpha_score)
    row_beta.score = int(new_beta_score)
    db.session.commit()
    return

@app.route('/results', methods=['GET','POST'])
def results():
    #votes = [vote.to_json() for vote in Votes.query.all()]
    characters = [character.character for character in Characters.query.all()]
    metrics = [metric.metric for metric in Polls.query.all()]

    initialise_Results_Table(characters, metrics)
    for vote in Votes.query.all():
        beta_character = vote.beta_character
        alpha_character = vote.alpha_character
        metric = vote.metric
        results_rows = [result for result in Results.query.all()]
        update_Results_table(results_rows,beta_character,alpha_character,metric)

    results = [result.to_json() for result in Results.query.all()]
    print(results[0])
    test_data = {
        "char1": results[0]['score'],
        "char2": results[1]['score'],
        "char3": results[2]['score'],
        }

    percents = [(result.score) for result in Results.query.all()]
    return render_template('results.html', title='Results Page', results = results, test_data = test_data,
    metrics = metrics, characters = characters, percents = percents)

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
    chars = [(x,x) for x in characters]
    form4.radio_button.choices = chars

    #let admins create new metrics to be voted on
    if form1.validate_on_submit():
        poll = Polls(user_id=current_user.username,
                     metric=form1.metric.data)

        db.session.add(poll)
        db.session.commit()
        flash('Poll created!')
        return redirect(url_for('admin_options'))

    #let admins delete metrics
    if form2.is_submitted():
        metric_to_delete = form2.radio_button.data
        for metric in Polls.query.all():
            if metric.metric == metric_to_delete:
                db.session.delete(metric)
                db.session.commit()
                flash('poll deleted!')

                #delete all instances of metric in the votes table
                counter = 0
                for vote in Votes.query.all():
                    if vote.metric == metric_to_delete:
                        db.session.delete(vote)
                        db.session.commit()
                        counter += 1
                flash(str(counter)+' instances of deletions in votes table')

                return redirect(url_for('admin_options'))



    #let admins create new characters to be voted

    if form3.validate_on_submit():
        new_character = Characters(user_id=current_user.username,
                     character=form3.character.data)
        db.session.add(new_character)
        db.session.commit()
        flash('Character added!')
        return redirect(url_for('admin_options'))


    #let admins delete characters
    if form2.is_submitted():
        char_to_delete = form4.radio_button.data
        for character in Characters.query.all():
            if character.character == char_to_delete:
                db.session.delete(character)
                db.session.commit()
                flash('character deleted!')

                #delete all instances of character in the votes table
                counter = 0
                for vote in Votes.query.all():
                    if vote.alpha_character == char_to_delete or vote.beta_character == char_to_delete:
                        db.session.delete(vote)
                        db.session.commit()
                        counter += 1
                flash(str(counter)+' instances of deletions in votes table')

                return redirect(url_for('admin_options'))


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

    num_metrics = len(metrics)
    num_characters = len(characters)

    #check if there are enough characters/metrics to have a vote
    if num_metrics >= 3 and num_characters >= 2:
        can_vote = True

        #GENERATES random selection of 10 metrics/character pairs
        random_pairs = random.sample(range(num_characters),num_characters)*5
        random_metrics = [0] + random.sample(range(num_metrics),num_metrics)*3
        #make sure we atleast cover the fixed 10 options

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


        #AGAIN MAJOR issues submitting forms dynamically so doing it for fixed amounts of votes.
        if form.is_submitted():
            count_votes = 0
            first_char = form.radio_button1.choices[0][1]
            second_char = form.radio_button1.choices[1][1]
            try:
                value = int(form.radio_button1.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button1.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button1.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 1 fail')

            first_char = form.radio_button2.choices[0][1]
            second_char = form.radio_button2.choices[1][1]
            try:
                value = int(form.radio_button2.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button2.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button2.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 2 fail')

            first_char = form.radio_button3.choices[0][1]
            second_char = form.radio_button3.choices[1][1]
            try:
                value = int(form.radio_button3.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button3.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button3.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 3 fail')

            first_char = form.radio_button4.choices[0][1]
            second_char = form.radio_button4.choices[1][1]
            try:
                value = int(form.radio_button4.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button4.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button4.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 1 fail')

            first_char = form.radio_button5.choices[0][1]
            second_char = form.radio_button5.choices[1][1]
            try:
                value = int(form.radio_button5.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button5.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button5.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 5 fail')

            first_char = form.radio_button6.choices[0][1]
            second_char = form.radio_button6.choices[1][1]
            try:
                value = int(form.radio_button6.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button6.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button6.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 6 fail')

            first_char = form.radio_button7.choices[0][1]
            second_char = form.radio_button7.choices[1][1]
            try:
                value = int(form.radio_button7.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button7.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button7.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 7 fail')

            first_char = form.radio_button8.choices[0][1]
            second_char = form.radio_button8.choices[1][1]
            try:
                value = int(form.radio_button8.data)
                if value == 1:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=first_char,
                                     beta_character=second_char,
                                     metric=form.radio_button8.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
                elif value == 2:
                    new_vote = Votes(
                                     user_id=current_user.id,
                                     alpha_character=second_char,
                                     beta_character=first_char,
                                     metric=form.radio_button8.label.text
                                     )
                    db.session.add(new_vote)
                    db.session.commit()
                    count_votes += 1
            except ValueError:
                print('button 8 fail')

            flash(str(count_votes) + " votes submitted!")
            return redirect(url_for('results'))

        else:
            print('fail')
            print(form.errors)

    else:
        can_vote = False

    return render_template('vote.html', title='Vote', form=form, metrics=metrics, characters=characters, can_vote = can_vote)

            #might need to indent this
