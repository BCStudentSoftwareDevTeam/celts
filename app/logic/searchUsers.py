from app.models.user import User

def searchUsers(query, phoneNumber):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    resultsDict = {}
    print(phoneNumber)

    firstName = splitSearch[0] + "%"
    lastName = " ".join(splitSearch[1:]) +"%"

    if len(splitSearch) == 1: #search for first or last name
        results = User.select().where(User.isStudent & (User.firstName ** firstName | User.lastName ** firstName))
        for participant in results:
            if participant not in resultsDict:
                resultsDict[f"{participant.firstName} {participant.lastName} ({participant.username})"] = f"{participant.firstName} {participant.lastName} ({participant.username})"
                if phoneNumber:
                    resultsDict[f"{participant.username} phoneNumber"] = participant.phoneNumber
    else:
        for searchTerm in splitSearch: #searching for specified first and last name
            if len(searchTerm) > 1:
                searchTerm += "%"
                results = User.select().where(User.isStudent & User.firstName ** firstName & User.lastName ** lastName)
                for participant in results:
                    if participant not in resultsDict:
                        resultsDict[f"{participant.firstName} {participant.lastName} ({participant.username})"] = f"{participant.firstName} {participant.lastName} ({participant.username})"
                        if phoneNumber:
                            resultsDict[f"{participant.username} phoneNumber"] = participant.phoneNumber

    return resultsDict
