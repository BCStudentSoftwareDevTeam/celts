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

# Update application config from config2
app.config.update(config.get())

# Override configuration with our local instance configuration
with open("app/config/" + app.config.override_file, 'r') as ymlfile:
    app.config.update(yaml.load(ymlfile, Loader=yaml.FullLoader))

# set the secret key after configuration is set up
app.secret_key = app.config['secret_key']

# Make 'env' a variable everywhere
@app.context_processor
def inject_environment():
    return dict(env=app.get_env())
