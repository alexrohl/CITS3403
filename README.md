# CITS3403
Project 2019
Started 5th May 2019. Alex Rohl (22233158) and Farruh Mavlonov (22252282)

may need to run in terminal:

virtual venv

source venv/bin/activate

pip install flask-sqlalchemy

pip install flask-migrate

pip install flask-login


Farruh's Job

Votes looks like
id, user_id, alpha, beta, metric
e.g. 1, 2, "Iron Man", "Thor", "Speed"
     2, 2, "Iron Man", "Hulk", "Speed"

Turn into Results table: id, character, metric, score
e.g. 1, "Iron Man", Speed, 1300
     2, "Thor", Speed, 1100

function initialise_Results_Table(list_of_characters, list_of_metrics):
  for metric in list_of_metrics
    for char in list_of_characters:
        new_row = Results(character = char, metric = metric, score = 1000)  #TABLENAME(field1='',field2='') makes a row  

        db.session.add(new_row)
        db.session.commit()

function update_elo(current_Results_Table, new_vote):
    >update table
    return Results_Table

function convert_old_votes_to_elo(initial_Results_Table, votes_table):
    initial_Results_Table()
    for vote in votes:
        update_elo(Results, vote)

OTHER JOBS
Make the website look cool
