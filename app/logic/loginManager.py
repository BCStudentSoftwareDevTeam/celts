from flask import request, session, abort
from peewee import DoesNotExist

from app import app
from app.models.user import User
from app.models.term import Term


def logout():
    """
        Erases the session and returns the URL for redirection
    """
    if 'username' in session:
        print("Logging out", session['username'])
    session.clear()

    url ="/"
    if app.config['use_shibboleth']:
        url = "/Shibboleth.sso/Logout"
    return url

def getUsernameFromEnvironment():
    if "username" in session:
        username = session["username"]

    shibKey = "eppn"
    if app.config['use_shibboleth']:
        if not shibKey in request.environ:
            print("No Shibboleth session present! Aborting")
            abort(403)

        username = request.environ[shibKey].split("@")[0].split('/')[-1].lower()
        return username

    else:
        return app.config['default_user']

def getLoginUser():
    username = getUsernameFromEnvironment()

    try:
        user = User.get_by_id(username)
    except DoesNotExist as e:
        # Create the user from Shibboleth
        # FIXME We need to identify the proper shibboleth attributes to insert into user
        user = User.create(
            username=username,
            firstName="Not",
            lastName="Yet",
            email=f"{username}@berea.edu",
            bnumber="B00055555")

    if 'username' not in session:
        print("Logging in as", user.username)
        session['username'] = user.username

    return user

def getCurrentTerm():
    return Term.get_or_none(isCurrentTerm = True)
