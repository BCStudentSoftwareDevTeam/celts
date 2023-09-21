import requests
import json
from collections import defaultdict

def callLsfApi(bNumber):
    """
    Make a call to the LSF endpoint which returns a specific students labor information.  

    The returned data is a dictionary with B# key and value that is a list of dicts that contain the labor information. 

    term code 13 summer 00 AY 

    """
    try: 
        lsfUrl = f"http://172.31.2.114:8080/api/usr/{bNumber}"
        response = requests.get(lsfUrl)
        return(response.json())
    except json.decoder.JSONDecodeError: 
        return {}

def getPositionAndTerm(user):
    studentLabor = callLsfApi(user.bnumber)

    for key, value in studentLabor.items(): 
        studentLabor[key] = [termCode for termCode in value if str(termCode["termCode"])[-2:] in ["00","13"]]

    studentDict = defaultdict(list)
    for key, value in studentLabor.items(): 
        for termCode in value:
            positionTitle = termCode['positionTitle']
            termName = termCode['termName']
            if positionTitle:
                studentDict[positionTitle].append(termName)

    return studentDict
