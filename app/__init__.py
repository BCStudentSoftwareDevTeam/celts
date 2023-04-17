import os
import pprint

from flask import Flask, render_template
from flask.helpers import get_env
from playhouse.shortcuts import model_to_dict, dict_to_model

import yaml

# Initialize our application
app = Flask(__name__, template_folder="templates")

######### Set up Application Configuration #############
# Uses config2 - https://pypi.org/project/config2/ - with the addition of an uncommitted
# override yml to set instance parameters. By default, 'local-override.yml'
#
# Precedence of configuration values is as follows:
#
# local-override.yml
#     ↓
# environment file (e.g., development.yml, production.yml)
#     ↓
# default.yml
#
##########################################################

# load in default
# with open(environment_file) as ymlfile:
# deep_update(override with ymlfile)
# with open(local_override) as ymlfile:
# deep_update(override with ymlfile)
from app.logic.utils import deep_update
os.environ["ENV"] = get_env()
with open("app/config/default.yml", 'r') as ymlfile:
    try:
        app.config.update(deep_update(app.config, yaml.load(ymlfile, Loader=yaml.FullLoader)))
    except TypeError:
        print("There was an error loading the override config file default.yml. It might just be empty.")
with open("app/config/" + [os.environ["ENV"]]+ ".yml", 'r') as ymlfile:
    try:
        app.config.update(deep_update(app.config, yaml.load(ymlfile, Loader=yaml.FullLoader)))
    except TypeError:
        print(f"There was an error loading the override config file " + [os.environ["ENV"]]+ ".yml. It might just be empty.")

# Override configuration with our local instance configuration
with open("app/config/" + app.config['override_file'], 'r') as ymlfile:
    try:
        app.config.update(deep_update(app.config, yaml.load(ymlfile, Loader=yaml.FullLoader)))
    except TypeError:
        print("There was an error loading the override config file " + app.config["override_file"] + ". It might just be empty.")

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
