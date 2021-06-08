from flask import Flask
from flask.helpers import get_env
from config2.config import config
import os
import yaml

# Initialize our application
app = Flask(__name__)

######### Set up App Configuration #############
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
################################################

# ensure ENV matches flask environment (for config2)
os.environ["ENV"] = get_env()

# Update application config from config2
app.config.update(config.get())

# Override configuration with our local instance configuration
with open("app/config/" + config.override_file, 'r') as ymlfile:
    try:
        app.config.update(yaml.load(ymlfile, Loader=yaml.FullLoader))
    except TypeError:
        print(f"There was an error loading the override config file {config.override_file}. It might just be empty.")

# set the secret key after configuration is set up
app.secret_key = app.config['secret_key']

# Make 'ENV' a variable everywhere
@app.context_processor
def inject_environment():
    return dict(ENV=get_env())
