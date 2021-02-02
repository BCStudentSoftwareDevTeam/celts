import pyodbc

details = {
    "user": "ute_limited",
    "password": "VB6PlU$WcbDBqZ3m0IDX",
    "server": "timemachine1sql.berea.edu",
    "db": "UTE"
}

# works
pyodbc_uri = 'DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['server'],details['db'],details['user'],details['password'])
# works
#pyodbc_uri = 'DRIVER=FreeTDS;DSN=tracyDSN;UID={};PWD={};'.format(details['user'], details['password'])
pyconn = pyodbc.connect(pyodbc_uri)
c = pyconn.cursor()
for row in c.execute('select * from STUPOSN'):
    print("PYODBC:",row)
    break

##########

from urllib.parse import quote
import sqlalchemy

# SAWarning: No driver name specified; this is expected by PyODBC when using DSN-less connections
#uri = "mssql+pyodbc://{}:{}@{}/{}".format(details['user'], details['password'], details['server'], details['db'])

# No driver name specified
#uri = "mssql+pyodbc://{}:{}@{}/{}?DRIVER=FreeTDS".format(details['user'], details['password'], details['server'], details['db'])
uri = "mssql+pyodbc:///?odbc_connect=" + quote('DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['server'],  details['db'], details['user'], details['password']))

engine = sqlalchemy.create_engine(uri)
for row in engine.execute('select * from STUPOSN'):
    print("SQLALCHEMY:",row)
    break

##########

from flask_sqlalchemy import SQLAlchemy
from app import load_config, app
from app.logic.tracy import Tracy

cfg = load_config('app/config/secret_config.yaml')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

uri = "mssql+pyodbc:///?odbc_connect=" + quote('DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['server'],  details['db'], details['user'], details['password']))

app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

print("FLASK:",Tracy().getPositionFromCode("S01015"))
