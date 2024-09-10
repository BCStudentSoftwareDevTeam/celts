from collections import defaultdict
from typing import List, Dict
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn, Case, DoesNotExist

from app.models.user import User
from app.models.term import Term

def getGraduatedStudents():
    """
        Get all the users who graduated
    """
    graduatedStudents = User.select().where(User.hasGraduated)

    return graduatedStudents