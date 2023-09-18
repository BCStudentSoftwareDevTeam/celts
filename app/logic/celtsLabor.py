import requests
import json

def callLsfApi(bNumber):
    """
    Make a call to the LSF endpoint which returns a specific students labor information.  

    The returned data is a dictionary with B# key and value that is a list of dicts that contain the labor information. 
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