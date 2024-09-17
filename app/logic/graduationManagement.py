from collections import defaultdict
from typing import List, Dict
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn, Case, DoesNotExist

from app.models.user import User
from app.models.term import Term


def getGraduatedStudent(username):
    """
    This function marks students as graduated
    Parameters:
    username: username of the user graduating
    """
    gradStudent = User.get(User.username == username)
    if gradStudent:
        gradStudent.hasGraduated = True
        gradStudent.save()
        return True
    return False

def removeGraduatedStudent(username):
    """
    This function unmarks students as graduated
    Parameters:
    username: username of the user graduating

    """
    notGradStudent = User.get(User.username == username)
    if notGradStudent:
        notGradStudent.hasGraduated = False
        notGradStudent.save()
        return True
    return False

def getAllTerms():
    """
        Return a list of all terms
    """
    allTerms = list(Term.select().order_by(Term.termOrder))

    return allTerms