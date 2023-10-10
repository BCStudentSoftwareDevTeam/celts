import requests
import json
from collections import defaultdict

def getStudentFromLsf(bNumber):
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
    """
    Parse the LSF response object so that it is only labor records for summer and academic years.

    Returned: defaultdict(<class 'list'>, {'positionTitle': ['termName'], 
                                           'positionTitle': ['termName'], 
                                           'positionTitle': ['termName', 'termName']
                                           })
    """
    studentLabor = getStudentFromLsf(user.bnumber)

    for key, value in studentLabor.items(): 
        # All term codes for summer end with 13 and all term codes for an academic year end in 00.
        studentLabor[key] = [termCode for termCode in value if str(termCode["termCode"])[-2:] in ["00","13"]]

    studentDict = defaultdict(list)
    for key, value in studentLabor.items(): 
        for termCode in value:
            positionTitle = termCode['positionTitle']
            termName = termCode['termName']
            if positionTitle:
                studentDict[positionTitle].append(termName)
    print(studentDict)
    return studentDict

def getAllCeltsLaborFromLsf():
    """
    Make a call to the LSF endpoint which returns all students and their labor records within the CELTS department. 

    The returned data is a dict with keys of B#'s and a value which is a list of dicts which is the the students labor information.

    """
    try: 
        lsfUrl = f"http://172.31.2.114:8080/api/org/{2084}"
        response = requests.get(lsfUrl)
        lsfResponseObj = response.json())
    except json.decoder.JSONDecodeError: 
        return {}
    # TODO: Parse lsfResponseObj so that it is only students who have records in CELTS. 
    # TODO: Save the parsed data to database. 