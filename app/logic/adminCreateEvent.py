from app.models import*
from app.models.term import Term
from app.models.user import User


def getTerms():

    listOfTerms = [term for term in Term.select()]
    return listOfTerms

def getFacilitators():

    facilitators = User.select(User).where((User.isFaculty == 1) | (User.isCeltsAdmin == 1) | (User.isCeltsStudentStaff == 1))
    return facilitators
