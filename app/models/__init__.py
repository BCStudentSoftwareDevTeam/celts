from peewee import *
import os

# from app import login
from app import app


def getMySQLDB():
    if os.environ.get("USING_CONTAINER", False):
        app.config['db']['host'] = 'db'
    else:
        app.config["db"]["host"] = "localhost"
    db_cfg = app.config['db']
    theDB = MySQLDatabase(db_cfg['name'], host = db_cfg['host'], user = db_cfg['username'], passwd = db_cfg['password'])
    return theDB

mainDB = getMySQLDB() # MySQL (current)

class baseModel(Model):
    class Meta:
        database = mainDB
