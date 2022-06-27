from playhouse.shortcuts import model_to_dict
from app.models.user import User
def searchUsers(query, searchvalue):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    resultsDict = {}

    firstName = splitSearch[0] + "%"
    lastName = " ".join(splitSearch[1:]) +"%"

    if len(splitSearch) == 1: #search for first or last name
        if searchvalue =="searchInstructor":
            results = User.select().where( User.isFaculty & (User.firstName ** firstName | User.lastName ** firstName))
        else:

            results = User.select().where(User.isStudent & (User.firstName ** firstName | User.lastName ** firstName))
        for participant in results:
            if participant not in resultsDict:
                resultsDict[participant.username]=model_to_dict(participant)
    else:
        for searchTerm in splitSearch: #searching for specified first and last name
            if len(searchTerm) > 1:
                searchTerm += "%"
                results = User.select().where(User.isStudent & User.firstName ** firstName & User.lastName ** lastName)
                for participant in results:
                    if participant not in resultsDict:
                        resultsDict[participant.username]=model_to_dict(participant)

    return resultsDict
