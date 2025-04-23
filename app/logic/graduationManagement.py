import xlsxwriter
from app import app
from peewee import JOIN

from app.models.user import User
from app.models.bonnerCohort import BonnerCohort
from app.logic.minor import getMinorProgress

def getGraduationManagementUsers():
    """
    Function to fetch all senior students along with their CCE Minor Progress and Bonner Status 
    """

    eligibleUsers = (User.select(User.username, User.hasGraduated, User.classLevel, User.firstName, User.lastName, BonnerCohort.year)
                 .join(BonnerCohort, JOIN.LEFT_OUTER, on=(BonnerCohort.user == User.username))
                 .where((User.classLevel == 'Senior') | (User.classLevel == "Graduating") | (User.processedClassLevel == "Graduated")))

    cceStudents = set([user["username"] for user in getMinorProgress()])

    graduationManagementUsers = []
    for user in eligibleUsers:
        userDict = user.__dict__
        graduationManagementUsers.append({
            "user": user,
            "cohort": userDict['bonnercohort'].year if 'bonnercohort' in userDict else None,
            "minorProgress": user.username in cceStudents})

    return graduationManagementUsers


def setGraduatedStatus(username, status):
    """
    Update a students graduation status based on the parameter status.
    """
    gradStudent = User.get(User.username == username)
    
    # it is necessary we cast this to an int instead of a bool because the
    # status is passed as a string and if we cast it to a bool it will always be True
    gradStudent.hasGraduated = int(status)

    if int(status) == 1:
        gradStudent.classLevel = "Graduated"
    else:
        gradStudent.classLevel = "Senior"

    gradStudent.save()
 