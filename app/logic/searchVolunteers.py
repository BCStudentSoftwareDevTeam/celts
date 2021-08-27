from app.models.user import User
from app.controllers.main import main_bp
from flask import json, jsonify



def searchVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    resultsDict = {}

    firstName = splitSearch[0] + "%"
    lastName = " ".join(splitSearch[1:]) +"%"

    if len(splitSearch) == 1: #search for first or last name
        results = User.select().where(User.isStudent & User.firstName ** firstName | User.lastName ** firstName)
        for participant in results:
            if participant not in resultsDict:
                resultsDict[f"{participant.firstName} {participant.lastName} ({participant.username})"] = f"{participant.firstName} {participant.lastName} ({participant.username})"
    else:
        for searchTerm in splitSearch: #searching for specified first and last name
            if len(searchTerm) > 1:
                searchTerm += "%"
                results = User.select().where(User.isStudent & User.firstName ** firstName & User.lastName ** lastName)
                for participant in results:
                    if participant not in resultsDict:
                        resultsDict[f"{participant.firstName} {participant.lastName} ({participant.username})"] = f"{participant.firstName} {participant.lastName} ({participant.username})"

    dictToJSON = json.dumps(resultsDict)
    print("dictToJSON.........",dictToJSON)
    return dictToJSON
