from app.models.user import User

def updateMinorInterest(username):
    user = User.get(username=username)
    print(user.minorInterest)
    user.minorInterest = not user.minorInterest
    if user.minorInterest == True:
        user.minorStatus = "Interested"
    else:
        user.minorStatus = "No interest"
    print(user.minorInterest)

    user.save()
