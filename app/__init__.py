import os

from flask import Flask
from flask.helpers import get_env
from playhouse.shortcuts import model_to_dict, dict_to_model

from config2.config import config
import yaml

# Initialize our application
app = Flask(__name__, template_folder="templates")

### Set up Celery
from celery import Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
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

# ensure ENV matches flask environment (for config2)
os.environ["ENV"] = get_env()

# Update application config from config2
app.config.update(config.get())

# Override configuration with our local instance configuration
from app.logic.utils import deep_update
with open("app/config/" + config.override_file, 'r') as ymlfile:
    try:
        deep_update(app.config, yaml.load(ymlfile, Loader=yaml.FullLoader))
    except TypeError:
        print(f"There was an error loading the override config file {config.override_file}. It might just be empty.")

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
