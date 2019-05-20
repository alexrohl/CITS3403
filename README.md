# CITS3403
Project 2019
Started 5th May 2019. Alex Rohl (22233158) and Farruh Mavlonov (22252282)

We outline the following:
1) the purpose of the web application, explaining both the context and the social choice mechanism used.
2) the architecture of the web application
3) describe how to launch the web application.
4) Include commit logs, showing contributions and review from both contributing students

1) The purpose of our web application is to allow users to rank marvel characters with respect to certain metrics. Characters and metrics can be added and deleted at any time through the admin options. Users will be prompted to vote for 8 random head to head comparisons for a random selection of metrics. Consequently, the results tables are calculated via an Elo Ranking system based off the head to head voting. The reason we have chosen this is to rank characters is that over time, all characters should receive an equal number of votes and hence producing a fair comparison across the board from 1st place to last place. (In contrast to preferential voting where typically only the top characters will receive votes and it is difficult to distinguish rankings among lesser characters who receive limited votes).

2) Our web application is made through the Python and Flask framework. We have based the structure of our application from Miguel Grinberg's 'The Flask Mega-Tutorial': https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

3) To launch our application, clone from: https://github.com/alexrohl/CITS3403.
   In the cloned directory, using terminal you may need to run the following:
    virtual venv
    source venv/bin/activate
    pip install flask-sqlalchemy
    pip install flask-migrate
    pip install flask-login
    pip install flask-wtf
    pip install python-dotenv

    !! may have to set: FLASK_APP=microblog.py

    Then simply run 'flask run' in terminal and follow the instructions to run on your local host

4) Git logs:
e77d30f - Alex Rohl, 20 minutes ago : Results now have an indicator of first place
f8413c7 - Alex Rohl, 76 minutes ago : merge
82072e2 - Farruh, 77 minutes ago : styling update 2
f12e366 - Farruh, 3 hours ago : styling updates
0eef691 - Farruh, 12 hours ago : heroku _init_.py changes
5466551 - Farruh, 35 hours ago : heroku deployment changes
7483c3b - Farruh, 2 days ago : python3
0587c63 - Alex Rohl, 2 days ago : Can now submit less than 8 votes
73e3a8b - Alex Rohl, 2 days ago : added some changes to index
05cfaa6 - Alex Rohl, 2 days ago : updated random voting options and added footer
d232b4a - Alex Rohl, 2 days ago : added visualisation to results section
dd1afdd - Farruh Mavlonov, 3 days ago : python3
d04fdd2 - Farruh Mavlonov, 3 days ago : edited read me
99dc1ae - Alex Rohl, 3 days ago : updated script.js
99a2bb6 - Alex Rohl, 3 days ago : updating script.js
dae86d1 - Alex Rohl, 3 days ago : moved script.js
c890e07 - Alex Rohl, 3 days ago : added basic barchart script
9c2eb09 - Alex Rohl, 3 days ago : ELO Ranking Working
9bfcb2f - Alex Rohl, 3 days ago : deleting characters/metrics now updates the votes table
4cd5628 - Alex Rohl, 3 days ago : Updated css to format banner nicely
6daa75d - Alex Rohl, 5 days ago : Can now delete characters and metrics from the admin view
daf111e - Alex Rohl, 5 days ago : Added admin options to add new characters
7b47ac7 - Alex Rohl, 8 days ago : Added existing polls/characters view in createpoll.html
67f2df4 - Alex Rohl, 8 days ago : multiple votes inputted working
9d947cb - Alex Rohl, 8 days ago : now 10 random pairs appear for the user to vote!
2ff4de8 - Alex Rohl, 8 days ago : Voting Form Working!
85dbb34 - Alex Rohl, 10 days ago : farruh see 'read me' file
f1db88e - Alex Rohl, 12 days ago : Can now vote for paired characters head to head
a348b6e - Alex Rohl, 12 days ago : Results page working now
60eb1f3 - Alex Rohl, 12 days ago : not working!
7443b5d - Farruh Mavlonov, 12 days ago : Add .gitignore
4dae69a - Alex Rohl, 12 days ago : Updating results.html
3b48acc - Farruh Mavlonov, 12 days ago : updated test.html
2f94369 - Farruh Mavlonov, 13 days ago : Test
f5ea0e9 - Farruh Mavlonov, 13 days ago : Initial commit
95e66a2 - Alex Rohl, 13 days ago : Added vote page
9d7b5fa - Alex Rohl, 13 days ago : added create poll page
6618780 - Alex Rohl, 13 days ago : Results page successfully showing
e4bc70c - Alex Rohl, 13 days ago : Added Results view
3691e31 - Alex Rohl, 2 weeks ago : deleted test file
e3a4c32 - Alex Rohl, 2 weeks ago : User Login
eafa248 - Alex Rohl, 2 weeks ago : first update commit
bf22941 - Alex Rohl, 2 weeks ago : first committed file
