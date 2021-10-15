from app.models.user import User

def addCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = True
    user.save()

def addCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = True
    user.save()

def removeCeltsAdmin(user):
    user = User.get_by_id(user)
    user.isCeltsAdmin = False
    user.save()

def removeCeltsStudentStaff(user):
    user = User.get_by_id(user)
    user.isCeltsStudentStaff = False
    user.save()

def changeCurrentTerm(term):
    termQuery = Term.select()
    oldCurrentTerm = Term.get_by_id(g.current_term)
    oldCurrentTerm.isCurrentTerm = False
    newCurrentTerm = Term.get_by_id(term)
    newCurrentTerm.isCurrentTerm = True
    termQuery.save()
