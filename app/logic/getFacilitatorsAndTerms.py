from app.models import*
from app.models.user import User
from app.models.term import Term

def getAllFacilitators():

    facilitators = User.select(User).where((User.isFaculty == 1) | (User.isCeltsAdmin == 1) | (User.isCeltsStudentStaff == 1))
    return facilitators

def selectFutureTerms(currentTermid):
    futureTerms = (Term.select().where(Term.id >= currentTermid)
                                .where((Term.year <= (Term.get_by_id(currentTermid)).year + 2)))

    return futureTerms
