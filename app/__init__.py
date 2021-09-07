import os

from flask import Flask
from flask.helpers import get_env

from config2.config import config
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


######### Blueprints #############
from app.controllers.admin import admin_bp as admin_bp
app.register_blueprint(admin_bp)

from app.controllers.events import events_bp as events_bp
app.register_blueprint(events_bp)

from app.controllers.main import main_bp as main_bp
app.register_blueprint(main_bp)
##################################

# Make 'ENV' a variable everywhere
@app.context_processor
def inject_environment():
    return dict( env=get_env() )

from app.logic.loginManager import getLoginUser
from flask import g
@app.before_request
def load_user():
    g.current_user = getLoginUser()

from app.logic.loginManager import getCurrentTerm
@app.before_request
def load_currentTerm():
    g.current_term = getCurrentTerm()
