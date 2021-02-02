from peewee import *
import os

# from app import login
from app import load_config


def getMySQLDB():
    cfg = load_config('app/config/secret_config.yaml')
    if os.environ.get("USING_CONTAINER", False):
        cfg['lsfdb']['host'] = 'db'
    else:
        cfg["lsfdb"]["host"] = "localhost"
    theDB = MySQLDatabase(cfg['lsfdb']['db_name'], host = cfg['lsfdb']['host'], user = cfg['lsfdb']['username'], passwd = cfg['lsfdb']['password'])
    return theDB

mainDB = getMySQLDB() # MySQL (current)

class baseModel(Model):
    class Meta:
        database = mainDB
