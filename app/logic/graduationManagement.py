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

    eligibleUsers = (User.select(User.username, User.hasGraduated, User.rawClassLevel, User.firstName, User.lastName, BonnerCohort.year)
                 .join(BonnerCohort, JOIN.LEFT_OUTER, on=(BonnerCohort.user == User.username))
                 .where((User.rawClassLevel == 'Senior') | (User.rawClassLevel == "Graduating") | (User.hasGraduated == True) ))

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
    Update a student's graduation status.
    """
    gradStudent = User.get(User.username == username)

    # it is necessary we cast this to an int instead of a bool because the
    # status is passed as a string and if we cast it to a bool it will always be True

    status = int(status)

    if status:
        # Mark as alumni
        gradStudent.hasGraduated = True
        gradStudent.rawClassLevel = "Graduating"
    else:
        # Revert to currently enrolled senior
        gradStudent.hasGraduated = False
        gradStudent.rawClassLevel = "Senior"

    gradStudent.save()

 