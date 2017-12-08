from flask import (Flask, render_template, request, redirect, jsonify,
                   url_for, flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Team, Player, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Premier League Player Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalogwithuser.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?grant_type=fb_exchan'
           'ge_token&client_id=%s&client_secret=%s&fb_exchange_token=%s') % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.8/me?access_token=%s&fields='
           'name,id,email') % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['access_token'] = token

    url = ('https://grap.facebook.com/v2.8/me/picture?access_token=%s&redirect'
           '=0&height=200&width=200') % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style = "width: 300px; height: 300px;border-radius: 150px;'
               '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> ')

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?'
           'access_token=%s') % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
                                            'connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style = "width: 300px; height: 300px;border-radius: 150px;-'
               'webkit-border-radius: 150px;-moz-border-radius: 150px;"> ')
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token '
                                            'for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/team/<int:team_id>/player/JSON')
def teamPlayerJSON(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    items = session.query(Player).filter_by(
        team_id=team_id).all()
    return jsonify(Players=[i.serialize for i in items])


@app.route('/team/<int:team_id>/player/<int:player_id>/JSON')
def playerJSON(team_id, player_id):
    player = session.query(Player).filter_by(id=player_id).one()
    return jsonify(Player=Player.serialize)


@app.route('/team/JSON')
def teamJSON():
    teams = session.query(Team).all()
    return jsonify(teams=[r.serialize for r in teams])


# Show all Teams
@app.route('/')
@app.route('/team/')
def showTeams():
    teams = session.query(Team).order_by(asc(Team.name))
    if 'username' not in login_session:
        return render_template('publicteams.html', teams=teams)
    else:
        return render_template('teams.html', teams=teams)


# Add a New Team
@app.route('/team/new/', methods=['GET', 'POST'])
def newTeam():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newTeam = Team(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newTeam)
        flash('New Team %s Successfully Created' % newTeam.name)
        session.commit()
        return redirect(url_for('showTeams'))
    else:
        return render_template('newTeam.html')


# Edit a Team
@app.route('/team/<int:team_id>/edit/', methods=['GET', 'POST'])
def editTeam(team_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedTeam = session.query(
        Team).filter_by(id=team_id).one()
    if editedTeam.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not author"
                "ized to edit this team. Please create your own team in order"
                " to edit.');}</script><body onload='myFunction()'>")
    if request.method == 'POST':
        if request.form['name']:
            editedTeam.name = request.form['name']
            flash('Team Successfully Edited %s' % editedTeam.name)
            return redirect(url_for('showTeams'))
    else:
        return render_template('editTeam.html', team=editedTeam)


# Delete a Team
@app.route('/team/<int:team_id>/delete/', methods=['GET', 'POST'])
def deleteTeam(team_id):
    if 'username' not in login_session:
        return redirect('/login')
    teamToDelete = session.query(
        Team).filter_by(id=team_id).one()
    if teamToDelete.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not authorized"
                " to delete this team. Please create your own team in order "
                "to delete.');}</script><body onload='myFunction()'>")
    if request.method == 'POST':
        session.delete(teamToDelete)
        flash('%s Successfully Deleted' % teamToDelete.name)
        session.commit()
        return redirect(url_for('showTeams', team_id=team_id))
    else:
        return render_template('deleteTeam.html', team=teamToDelete)


# Show all Players on a Team
@app.route('/team/<int:team_id>/')
@app.route('/team/<int:team_id>/player/')
def showPlayer(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    creator = getUserInfo(team.user_id)
    players = session.query(Player).filter_by(
        team_id=team_id).all()
    if 'username' not in login_session or creator.id != login_session['us'
                                                                      'er_id']:
        return render_template('publicplayer.html', players=players,
                               team=team, creator=creator)
    else:
        return render_template('player.html', players=players, team=team,
                               creator=creator)


# Add a New Player from a Team
@app.route('/team/<int:team_id>/player/new/', methods=['GET', 'POST'])
def newPlayer(team_id):
    if 'username' not in login_session:
        return redirect('/login')
    team = session.query(Team).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        return ("<script>function myFunction() {alert('You are not authorized"
                " to add players to this team. Please create your own team in"
                " order to add different players.');}</script><body "
                "onload='myFunction()'>")
    if request.method == 'POST':
        newPlayer = Player(name=request.form['name'],
                           yr_strtd=request.form['yr_strtd'],
                           origin=request.form['origin'],
                           position=request.form['position'],
                           team_id=team_id, user_id=team.user_id)
        session.add(newPlayer)
        session.commit()
        flash('New Player %s Successfully Created' % (newPlayer.name))
        return redirect(url_for('showPlayer', team_id=team_id))
    else:
        return render_template('newplayer.html', team_id=team_id)


# Edit a Player from a Team
@app.route('/team/<int:team_id>/player/<int:player_id>/edit',
           methods=['GET', 'POST'])
def editPlayer(team_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedPlayer = session.query(Player).filter_by(id=player_id).one()
    team = session.query(Team).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        return ("<script>function myFunction() {alert('You are not authorized"
                " to edit players to this team. Please create your own team in"
                " order to edit players.');}</script><body "
                "onload='myFunction()'>")
    if request.method == 'POST':
        if request.form['name']:
            editedPlayer.name = request.form['name']
        if request.form['yr_strtd']:
            editedPlayer.yr_strtd = request.form['yr_strtd']
        if request.form['origin']:
            editedPlayer.origin = request.form['origin']
        if request.form['position']:
            editedPlayer.position = request.form['position']
        session.add(editedPlayer)
        session.commit()
        flash('Player Successfully Edited')
        return redirect(url_for('showPlayer', team_id=team_id))
    else:
        return render_template('editplayer.html', team_id=team_id,
                               player_id=player_id, player=editedPlayer)


# Delete a Player from a Team
@app.route('/team/<int:team_id>/player/<int:player_id>/delete',
           methods=['GET', 'POST'])
def deletePlayer(team_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    team = session.query(Team).filter_by(id=team_id).one()
    playerToDelete = session.query(Player).filter_by(id=player_id).one()
    if login_session['user_id'] != team.user_id:
        return ("<script>function myFunction() {alert('You are not authorized"
                " to delete players on this team. Please create your own team"
                " to delete players.');}</script><body"
                " onload = 'myFunction()'> ")
    if request.method == 'POST':
        session.delete(playerToDelete)
        session.commit()
        flash('Player Successfully Deleted')
        return redirect(url_for('showPlayer', team_id=team_id))
    else:
        return render_template('deleteplayer.html', player=playerToDelete)


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showTeams'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showTeams'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=8000)
