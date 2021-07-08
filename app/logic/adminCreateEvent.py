from app.models import*
from app.models.term import Term
from app.models.user import User


def getTerms():

    listOfTerms = [term for term in Term.select()]
    # currentTerm = Term.select(Term.description).where(Term.isCurrentTerm == 1)
    # term = [t.description for t in currentTerm.objects()] #This could be done better. but how??
    return listOfTerms

def getFacilitators():

    facilitators = User.select(User).where((User.isFaculty == 1) | (User.isCeltsAdmin == 1) | (User.isCeltsStudentStaff == 1))
    return facilitators
