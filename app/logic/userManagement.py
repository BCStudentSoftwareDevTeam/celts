from app.models.user import User

def addCeltsAdmin(user):
    user = User.get_by_id(user)
    userSelect = User.get(User.username == user.username)
    userSelect.isCeltsAdmin = True
    userSelect.save()

def addCeltsStudentStaff(user):
    user = User.get_by_id(user)
    userSelect = User.get(User.username == user.username)
    userSelect.isCeltsStudentStaff = True
    userSelect.save()

def removeCeltsAdmin(user):
    user = User.get_by_id(user)
    userSelect = User.get(User.username == user.username)
    userSelect.isCeltsAdmin = False
    userSelect.save()

def removeCeltsStudentStaff(user):
    user = User.get_by_id(user)
    userSelect = User.get(User.username == user.username)
    userSelect.isCeltsStudentStaff = False
    userSelect.save()
