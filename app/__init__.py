import os
import pprint

from flask import Flask, render_template
from flask.helpers import get_env
from playhouse.shortcuts import model_to_dict, dict_to_model

# Initialize our application
app = Flask(__name__, template_folder="templates")

from app.logic.utils import load_config_files

env = get_env()

app.config.update(load_config_files(app.config, env))

# set the secret key after configuration is set up
app.secret_key = app.config['secret_key']

# These imports must happen after configuration
from app.models.term import Term
from app.models.user import User

from peewee import BaseQuery
if app.config['show_queries']:
    old_execute = BaseQuery.execute
    def new_execute(*args, **kwargs):
        if session:
            if 'querycount' not in session:
                session['querycount'] = 0

            session['querycount'] += 1
            print("**Running query {}**".format(session['querycount']))
            print(args[0])
        return old_execute(*args, **kwargs)
    BaseQuery.execute = new_execute


######### Blueprints #############
from app.controllers.admin import admin_bp as admin_bp
app.register_blueprint(admin_bp)

from app.controllers.events import events_bp as events_bp
app.register_blueprint(events_bp)

from app.controllers.main import main_bp as main_bp
app.register_blueprint(main_bp)

from app.controllers.serviceLearning import serviceLearning_bp as serviceLearning_bp
app.register_blueprint(serviceLearning_bp)
##################################

# Make 'ENV' a variable everywhere
@app.context_processor
def inject_environment():
    return dict( env=get_env() )

from flask import session
@app.before_request
def queryCount():
    if session:
        session['querycount'] = 0

from app.logic.loginManager import getLoginUser
from flask import g
@app.before_request
def load_user():
    # An exception handles both current_user not being set and a mismatch between models
    try:
        g.current_user = dict_to_model(User,session['current_user'])
    except Exception as e:
        user = getLoginUser()
        session['current_user'] = model_to_dict(user)
        g.current_user = user

from app.logic.loginManager import getCurrentTerm
@app.before_request
def load_currentTerm():
    # An exception handles both current_term not being set and a mismatch between models
    try:
        g.current_term = dict_to_model(Term, session['current_term'])
    except Exception as e:
        term = getCurrentTerm()
        session['current_term'] = model_to_dict(term)
        g.current_term = term

from flask import request
@app.context_processor
def load_visibleAccordion():
    acc = request.args.get("accordion", default = False)
    return {"visibleAccordion": acc}
"""
Error handling for all 403, 404, 500 errors. Works by rendering a customm html
file located at templates/errors. All abort calls are automatically routed here
to be handled.
"""

supportContactEmail = app.config["support_email_contact"]

@app.errorhandler(403)
def handle_bad_request(e):
    return render_template("/errors/403error.html",
                            supportEmail = supportContactEmail)

@app.errorhandler(404)
def handle_bad_request(e):
    return render_template("/errors/404error.html",
                            supportEmail = supportContactEmail)

@app.errorhandler(500)
def handle_bad_request(e):
    return render_template("/errors/500error.html",
                            supportEmail = supportContactEmail)
