from flask import Flask
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
os.environ["ENV"] = app.get_env()

app.config.update(config.get())
override_path = "app/config/" + app.config.override_file
try:
    with open(override_path, 'r') as ymlfile:
        app.config.update(yaml.load(ymlfile, Loader=yaml.FullLoader))
except FileNotFoundError e:
    Path(override_path).touch() # create it if it doesn't exist

app.secret_key = app.config['secret_key']

# Make 'env' a variable everywhere
@app.context_processor
def inject_environment():
    return dict(env=app.get_env())
