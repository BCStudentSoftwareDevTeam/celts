from app.models.user import User
from app.models.individualRequirement import IndividualRequirement
from app.models.certificationRequirement import CertificationRequirement

from peewee import *
from peewee import JOIN
from peewee import fn

def getMinorInterest():
    interestedStudents = User.select(User.firstName, User.lastName).where((User.isStudent == 1) & (User.minorInterest == 1))

    interestedStudentList = [{'firstName': student.firstName, 'lastName': student.lastName} for student in interestedStudents]

    return interestedStudentList

def getEngagedStudentsWithRequirementCount():
    engagedStudentsWithCount = (
        User
        .select(User.firstName, User.lastName, fn.COUNT(IndividualRequirement.id).alias('requirementCount'))
        .join(IndividualRequirement, on=(User.username == IndividualRequirement.username))
        .group_by(User.username)
        .order_by(fn.COUNT(IndividualRequirement.id).desc())
    )

    engagedStudentsList = [
        {
            'firstName': student.firstName,
            'lastName': student.lastName,
            'requirementCount': student.requirementCount
        }
        for student in engagedStudentsWithCount
    ]

    for student in engagedStudentsList:
        print(f"firstName: {student['firstName']}, lastName: {student['lastName']}, requirementCount: {student['requirementCount']}")

    return engagedStudentsList

