from ldap3 import Server, Connection, ALL
from peewee import *
from os import path, remove
from app.models.models import *
import argparse


# Create database connection and model
database_path = "LDAP.db"
database = SqliteDatabase(database_path)

class Faculty(Model):
    fID               = PrimaryKeyField()
    username          = CharField(unique = True)
    bnumber           = TextField(null = True)
    lastname          = TextField(null = True)
    firstname         = TextField(null = True)

    class Meta:
        database = database

class Staff(Model):
    sID               = PrimaryKeyField()
    username          = CharField(unique = True)
    bnumber           = TextField(null = True)
    lastname          = TextField(null = True)
    firstname         = TextField(null = True)
    class Meta:
        database = database
def connect_to_server(user,password):
    server = Server ('berea.edu', port=389, use_ssl=False, get_info='ALL')
    # conn   = Connection (server, user=skt['ldap']['user'], password=skt['ldap']['pass'])
    conn   = Connection (server, user=user, password=password)
    if not conn.bind():
        print(conn.result)
        raise Exception("BindError")
    return conn
