import requests
import json
from peewee import DoesNotExist

from collections import defaultdict
from app.models.user import User
from app.models.celtsLabor import CeltsLabor

def getCeltsLaborFromLsf():
    """
        Make a call to the LSF endpoint which returns a specific students labor information.  

        The returned data is a dictionary with B# key and value that is a list of dicts that contain the labor information. 

    """
    try: 
        # lsfUrl = f"http://172.31.2.114:8080/api/org/2084"
        lsfUrl = f"http://10.40.132.89:8080/api/org/2084"
        response = requests.get(lsfUrl)
        return(response.json())
    except json.decoder.JSONDecodeError: 
        return {}

def parseLsfResponse():
    """
        Parse the LSF response object so that it is only labor records for summer and academic years.

        Input: JSON response
                {'B#': [{'positionTitle': 'Position Title',
                         'termCode': 'Term Code', 
                         'laborStart': Labor Start Date, 
                         'laborEnd': Labor End Date, 
                         'jobType': 'Job Type',
                         'wls': 'WLS Lvl',
                         'termName': 'Term Name'}],
                 'B#': [{'positionTitle': 'Position Title',
                         'termCode': 'Term Code', 
                         'laborStart': Labor Start Date, 
                         'laborEnd': Labor End Date, 
                         'jobType': 'Job Type',
                         'wls': 'WLS Lvl',
                         'termName': 'Term Name'}]}
    """
    laborDict = getCeltsLaborFromLsf()

    studentLaborDict = {}
    for key, value in laborDict.items(): 
        try: 
            username = User.get(bnumber = key)
            # All term codes for summer end with 13 and all term codes for an academic year end in 00 and those are the only terms we want to record.
            studentLaborDict[username] = collapsePositions([p for p in value if str(p["termCode"])[-2:] in ["00","13"]])
        except DoesNotExist: 
            pass

    refreshCeltsLaborRecords(studentLaborDict)

def collapsePositions(positionList):
    '''
        Parse position information from the JSON response and return only the position title and term title 

        Input: [{'positionTitle': 'Position Title',
                 'termCode': 'Term Code', 
                 'laborStart': Labor Start Date, 
                 'laborEnd': Labor End Date, 
                 'jobType': 'Job Type',
                 'wls': 'WLS Lvl',
                 'termName': 'Term Name'}]
        
        Returned:{'Position Title': ['Term Name']}

    '''
    positionDict = defaultdict(list)

    for position in positionList:
        positionDict[position['positionTitle']].append(position['termName'])

    return positionDict

def refreshCeltsLaborRecords(laborDict):
    """
        Input: Dictionary containing CELTS labor information
                {'username1': {'positionTitle': ['termName'],
                               'positionTitle': ['termName']},
                'username2': {'positionTitle': ['termName', 'termName']}
                }

        Delete records for the students that are currently in the CeltsLabor table
        if they are also in the laborDict and save content of laborDict to the table. 
    """
    celtsLabor = []
    for key, value in laborDict.items():
        for positionTitle, termNames in value.items():
            for termName in termNames: 
                celtsLabor.append({"user": key,
                                   "positionTitle": positionTitle,
                                   "termName": termName})    

    CeltsLabor.delete().where(CeltsLabor.user << [username['user'] for username in celtsLabor]).execute()                         
    CeltsLabor.insert_many(celtsLabor).on_conflict_replace().execute()

def getCeltsLaborHistory(volunteer):
    
    laborHistoryList = list(CeltsLabor.select().where(CeltsLabor.user == volunteer).order_by(CeltsLabor.termName))
    
    laborHistoryDict= {}
    for position in laborHistoryList: 
        laborHistoryDict[position.positionTitle] = position.termName

    return laborHistoryDict