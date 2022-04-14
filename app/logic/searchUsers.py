from playhouse.shortcuts import model_to_dict
from app.models.user import User
from app.models.outsideParticipant import OutsideParticipant

def searchUsers(query,searchGroup):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    resultsDict = {}

    firstName = splitSearch[0] + "%"
    lastName = " ".join(splitSearch[1:]) +"%"
    results = None
    searchId = None
    print ("This.................",searchGroup)
    if len(splitSearch) == 1: #search for first or last name
        if searchGroup != "outsideParticipant":
            results = User.select().where(User.isStudent & (User.firstName ** firstName | User.lastName ** firstName))
        else:
            results = OutsideParticipant.select().where(OutsideParticipant.firstName ** firstName | OutsideParticipant.lastName ** firstName)

        for participant in results:
            if searchGroup != "outsideParticipant":
                searchId = participant.username
                if participant not in resultsDict:
                    resultsDict[participant.username]=model_to_dict(participant)
            else:
                searchId = participant.email
                if participant not in resultsDict:
                    resultsDict[participant.email]=model_to_dict(participant)


    else:
        for searchTerm in splitSearch: #searching for specified first and last name
            if len(searchTerm) > 1:
                searchTerm += "%"
                if searchGroup != "outsideParticipant":
                    searchId = participant.username
                    results = User.select().where(User.isStudent & (User.firstName ** firstName | User.lastName ** firstName))
                else:
                    searchId = participant.email
                    OutsideParticipant.select().where(OutsideParticipant.firstName ** firstName & OutsideParticipant.lastName ** lastName)
                for participant in results:
                    if participant not in resultsDict:
                        resultsDict[participant.username]=model_to_dict(participant)

    print(resultsDict, "ahaaammammmmmmmmmmmmmm.........")
    return resultsDict
