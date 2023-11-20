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

def getEngagedStudents():
    engagedStudents = (User
            .select(User.username, User.firstName, User.lastName)
            .join(IndividualRequirement, on=(User.username == IndividualRequirement.username))
            .distinct()  # To get unique combinations of students
            )
    engagedStudentList = [{'firstName': student.firstName, 'lastName': student.lastName} for student in engagedStudents]
    print(engagedStudentList)

    return engagedStudentList

def getRequirementCount():
    username_counts = (IndividualRequirement
                    .select(IndividualRequirement.username, fn.COUNT(IndividualRequirement.username).alias('count_alias'))
                    .group_by(IndividualRequirement.username))

    # Convert the query results to a list of dictionaries
    results_list = [
        {'username': result.username, 'count': result.count_alias}
        for result in username_counts
    ]

    # Display the list of dictionaries
    print(results_list)
    return results_list
