from app.models.user import User

def addCeltsAdmin(user):

    user = User.get_by_id(user)
    userSelect = User.get(User.username == user.username)
    userSelect.isCeltsAdmin = 1 
    userSelect.save()


def addCeltsStudentStaff(user):

    return 0

def removeCeltsAdmin(user):

    user = User.get_by_id(user)
    userSelect = User.get(User.username == user.username)
    userSelect.isCeltsAdmin = 0
    userSelect.save()

def removeCeltsStudentStaff(user):

    return 0
