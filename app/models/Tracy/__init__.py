from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import load_config, app
import urllib3
from urllib.parse import quote
import os

cfg = load_config('app/config/secret_config.yaml')

host = cfg['tracy']['host']
if not os.environ.get("USING_CONTAINER", False):
    host = "localhost"

# MySQL database connection
uri = "mysql+pymysql://{}:{}@{}/{}".format(cfg['tracy']['username'], cfg['tracy']['password'], host, cfg['tracy']['db_name'])

# MSSQL database connection
if app.config['use_tracy']:
    uri = "mssql+pyodbc:///?odbc_connect=" + quote('DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(cfg['tracy']['mssql_host'],  cfg['tracy']['db_name'], cfg['tracy']['mssql_user'], cfg['tracy']['mssql_password']))


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)
migrate = Migrate(app, db)
