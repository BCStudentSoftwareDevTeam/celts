import requests
import json
from peewee import DoesNotExist

from collections import defaultdict
from app.models.user import User
from app.models.celtsLabor import CeltsLabor

def getStudentFromLsf():
    """
    Make a call to the LSF endpoint which returns a specific students labor information.  

    The returned data is a dictionary with B# key and value that is a list of dicts that contain the labor information. 

    """
    try: 
        lsfUrl = f"http://172.31.2.114:8080/api/org/{2084}"
        response = requests.get(lsfUrl)
        return(response.json())
    except json.decoder.JSONDecodeError: 
        return {}

def getPositionAndTerm():
    """
    Parse the LSF response object so that it is only labor records for summer and academic years.

    Input: json response object

    """
    laborDict = getStudentFromLsf()

    sutdentLaborDict = {}
    for key, value in laborDict.items(): 
        # All term codes for summer end with 13 and all term codes for an academic year end in 00.
        try: 
            username = User.get(bnumber = key)
            sutdentLaborDict[username] = collapsePositions([p for p in value if str(p["termCode"])[-2:] in ["00","13"]])
        except DoesNotExist: 
            pass
    saveLaborToDb(sutdentLaborDict)

def collapsePositions(positionList):
    positionDict = defaultdict(list)

    for position in positionList:
        positionDict[position['positionTitle']].append(position['termName'])
    
    return positionDict

def saveLaborToDb(laborDict):
    """
    Save the Labor Position info gotten from LSF to CELTS DB 
    """
    celtsLabor = []

    for key, value in laborDict.items():
        for positionTitle, termNames in value.items():
            for termName in termNames: 
                celtsLabor.append({"user": key,
                                   "positionTitle": positionTitle,
                                   "termName": termName})    
                             
    CeltsLabor.insert_many(celtsLabor).on_conflict_replace().execute()