from app.models import*
from app.models.term import Term
from app.models.user import User


def getTermDescription():

    termDescriptions = Term.select(Term.description)
    descriptions = [des.description for des in termDescriptions.objects()]

    return descriptions

def getCurrentTerm():

    currentTerm = Term.select(Term.description).where(Term.isCurrentTerm == 1)
    term = [t.description for t in currentTerm.objects()] #This could be done better. but how??
    return term[0]

def getFacilitators():

    facilitators = User.select(User).where((User.isFaculty == 1) | (User.isCeltsAdmin == 1) | (User.isCeltsStudentStaff == 1))
    listOfFacilitators = [fac for fac in facilitators.objects()]
    return listOfFacilitators
