from app.models.user import User
from peewee import *


def getMinorInterest():
    interestedStudents = User.select(User.firstName, User.lastName).where((User.isStudent == 1) & (User.minorInterest == 1))

    studentList = [{'firstName': student.firstName, 'lastName': student.lastName} for student in interestedStudents]

    return studentList