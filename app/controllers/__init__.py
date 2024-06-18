# from app import app
# import os
# # from app.login_manager import require_login


# @app.context_processor
# def injectGlobalData():
#     currentUser = require_login()
#     lastStaticUpdate = str(max(os.path.getmtime(os.path.join(root_path, f))
#                  for root_path, dirs, files in os.walk('app/static')
#                   for f in files))
#     return {'currentUser': currentUser,
#            'lastStaticUpdate': lastStaticUpdate}
import os
import pprint
from flask import Flask, render_template
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.logic.config import load_config_files
# Initialize our application
app = Flask(__name__, template_folder="templates")
app.env = os.environ.get('APP_ENV', 'production')
load_config_files(app)
print (" * Environment:", app.env)
# set the secret key after configuration is set up
app.secret_key = app.config['secret_key']
# These imports must happen after configuration
from app.models.term import Term
from app.models.user import User
from peewee import BaseQuery
from flask import session