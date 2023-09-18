import requests
import json

def callLsfApi(bNumber):
    """
    Make a call to the LSF endpoint which returns every students labor info. 

    The data is a dictionary with keys that are B#s and values that are lists of dicts which contain labor information
    {"B#":[{"jobType":"Primary",
            "laborEnd":"Mon, 18 Jul 2016 00:00:00 GMT",
            "laborStart":"Mon, 23 May 2016 00:00:00 GMT",
            "positionTitle":"Habitat for Humanity Coord.",
            "termCode":201513,
            "termName":"Summer 2016",
            "wls":"5"},
            {"jobType":"Primary",
            "laborEnd":"Tue, 13 Dec 2016 00:00:00 GMT","
            laborStart":"Tue, 23 Aug 2016 00:00:00 GMT",
            "positionTitle":"Habitat for Humanity Coord.",
            "termCode":201611,
            "termName":"Fall 2016","wls":"5"}]
    """
    try: 
        lsfUrl = f"http://172.31.2.114:8080/api/usr/{bNumber}"
        response = requests.get(lsfUrl)
        return(response.json())
    except json.decoder.JSONDecodeError: 
        return {}

def getPositionAndTerm(user):
    studentLabor = callLsfApi(user.bnumber)

    studentDict = {}
    for key, value in studentLabor.items(): 
        for termCode in value:
            positionTitle = termCode['positionTitle']
            termName = termCode['termName']
            if positionTitle in studentDict:
                studentDict[positionTitle].append(termName)
            else:
                studentDict[positionTitle] = [termName]

    return studentDict