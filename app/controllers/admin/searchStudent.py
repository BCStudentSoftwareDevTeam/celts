from app.models.user import User
from peewee import *


def searchStudent():
    students = User.select()
    return studentSearch
