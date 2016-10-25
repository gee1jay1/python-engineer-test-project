"""Flask Module to define and implement REST API to retrieve and add
data regarding teams, users and companies.
"""


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import ujson as json


# Set up app data.
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Team(db.Model):
    """Database model to store teams and their info."""
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    members = db.relationship('User', backref='team')


class User(db.Model):
    """Database model to store users and their info."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))


class Company(db.Model):
    """Database model to store companies and their info."""
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    users = db.relationship('User', backref='company')


def get_all_teams():
    """Retrieve all Teams from the database."""
    all_teams = Team.query.all()
    return all_teams


def get_team_by_name(name):
    """Retrieve the Team from the database with the given name."""
    team = Team.query.filter_by(name=name)
    return team


def get_team_by_company(companyname):
    """Retrieve the Teams from the database containing the users who have
     the given company name.
    """
    filtered_teams = []
    teams = get_all_teams()

    for team in teams:
        for member in team.members:
            if (member.company.name == companyname and
                    (team not in filtered_teams)):
                filtered_teams.append(team)

    return filtered_teams


def teams_to_json(teams):
    """Given a set of SQLAlchemy query Team results, put them into
    a consistent JSON format.
    """
    team_json = []
    for team in teams:
        team_dict = {}
        team_dict['id'] = team.id
        team_dict['name'] = team.name

        # We dump the json when we return so don't want to dump
        # in the user level function as well.
        team_dict['members'] = users_to_json(team.members, dump=False)
        team_json.append(team_dict)

    return json.dumps(team_json)


def users_to_json(users, dump=True):
    """Given a set of SQLAlchemy query User results, put them into
    a consistent JSON format.
    """
    user_json = []
    for user in users:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['name'] = user.name
        user_dict['company'] = company_to_json(user.company, dump=False)
        user_dict['email'] = user.email
        user_json.append(user_dict)
    return json.dumps(user_json) if dump else user_json


def company_to_json(company, dump=True):
    """Given a Company SQLAlchemy query result, put into a
    consistent JSON format.
    """
    company_dict = {}
    company_dict['name'] = company.name
    company_dict['id'] = company.id
    return json.dumps(company_dict) if dump else company_dict


def add_post_json(json_data):
    """Add JSON data received from a post to the database.
    Assumes data received is of correct format.
    """
    # Better, more generic way of doing this?
    companies = []
    users = []
    team = Team(name=json_data['name'])
    for member in json_data['members']:
        company = Company(name=member['company'])
        if company not in companies:
            companies.append(company)

        users.append(User(name=member['name'], email=member['email'],
                     company=company, team=team))

    db.session.add(team)
    db.session.add_all(companies)
    db.session.add_all(users)


@app.route('/teams', methods=['GET'])
def teams():
    """Route to return all teams in the database."""
    teams = get_all_teams()
    return teams_to_json(teams)


@app.route('/team/<teamname>', methods=['GET'])
def team_by_name(teamname):
    """Route to return a named team from the database."""
    team = get_team_by_name(teamname)
    return teams_to_json(team)


@app.route('/company/<companyname>', methods=['GET'])
def teams_by_company(companyname):
    """Route to return teams associated with a named company
    from the database."""
    teams = get_team_by_company(companyname)
    return teams_to_json(teams)


@app.route('/add/team', methods=['POST'])
def add_team():
    """Route to allow external user to POST JSON to be stored
    in the database.
    """
    post_data = request.json
    add_post_json(post_data)
    return 'Added Team'


def add_test_data():
    """Add some test data of all types to populate the database at
    start of day.
    """
    def_jam = Company(name="Def_Jam_Records")
    ruthless = Company(name="Ruthless_Records")
    nwa = Team(name='NWA')
    gfunk = Team(name='GFUNK')
    users_to_commit = []
    users_to_commit.append(User(name="Ice Cube", email="icecube@gmail.com",
                                team=nwa, company=ruthless))
    users_to_commit.append(User(name="MC Ren", email="ren@hotmail.com",
                                team=nwa, company=ruthless))
    users_to_commit.append(User(name="Warren G", email="warren@gmail.com",
                                team=gfunk, company=def_jam))
    users_to_commit.append(User(name="Nate Dogg", email="nate@gmail.com",
                                team=gfunk, company=def_jam))

    db.session.add(def_jam)
    db.session.add(ruthless)
    db.session.add(nwa)
    db.session.add(gfunk)
    db.session.add_all(users_to_commit)
    db.session.commit()


if __name__ == '__main__':

    # Create the database tables.
    db.drop_all()
    db.create_all()

    # Add some test data.
    add_test_data()

    # Start the app.
    app.run(host='0.0.0.0')
