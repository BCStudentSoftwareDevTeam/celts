import requests
import json
from peewee import DoesNotExist
from collections import defaultdict
from app import app
from app.models.user import User
from app.models.celtsLabor import CeltsLabor
from app.models.term import Term

def getCeltsLaborFromLsf():
    """
        Make a call to the LSF endpoint which returns all CELTS student labor records. 

        The returned data is a dictionary with B# key and value that is a list of dicts that contain the labor information. 

    """
    try: 
        lsfUrl = f"{app.config['lsf_url'].strip('/')}/api/org/2084"
        response = requests.get(lsfUrl)
        return response.json()
    except json.decoder.JSONDecodeError: 
        print(f'Response from {lsfUrl} was not JSON.\n' + response.text)
        return {}
    except KeyError as e: 
        print(f'Make sure you have "lsf_url" set in your local-override config file.')
        raise(e)

def updateCeltsLaborFromLsf():
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
    # laborDict = getCeltsLaborFromLsf()
    # print("your the badest:", laborDict)  
    # print("panorama:", type(laborDict))        
    laborDict = { 'B00794020': [
            {
                'jobType': 'Primary',
                'laborEnd': '2025-12-13',
                'laborStart': '2025-08-19',
                'positionTitle': 'Hispanic Outreach Associate',
                'termCode': 202400,
                'termName': 'Fall 2024',
                'wls': '4'
            }            
        ],
        'b00815939': [
            {
                'jobType': 'Primary',
                'laborEnd': '2025-12-13',
                'laborStart': '2025-08-19',
                'positionTitle': 'Hispanic Outreach Associate',
                'termCode': 202400,
                'termName': 'Fall 2024',
                'wls': '4'
            }            
        ]
    }
    
    studentLaborDict = {}
    for key, value in laborDict.items(): 
        try: 
            username = User.get(bnumber = key)
            print(f"found user: {username} for key: {key}")
            # All term codes for summer end with 13 and all term codes for an academic year end in 00 and those are the only terms we want to record.
            filtered = [p for p in value if str(p["termCode"])[-2:] in ["00","11"]]
            print(f"filterd positions: {filtered}")
            studentLaborDict[username] = collapsePositions(filtered)
        except DoesNotExist: 
            print(f"user not found for bnumber: {key}")

        print ("final labordict:", studentLaborDict)

   

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
    laborPositionDict = defaultdict(list)

    for position in positionList:
        laborPositionDict[position['positionTitle']].append(position['termName'].replace("AY ", ""))

    return laborPositionDict

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
            for term in termNames: 
                termTableMatch = Term.select() 
                if term[0].isalpha(): 
                    termTableMatch = termTableMatch.where(Term.description == term)
                else:
                    termTableMatch = termTableMatch.where(Term.academicYear == term, Term.description % "Fall%")
                try:
                    laborTerm = termTableMatch.get()
                    isAcademicYear = not laborTerm.isSummer
                    celtsLabor.append({"user": key,
                                       "positionTitle": positionTitle,
                                       "term": laborTerm,
                                       "isAcademicYear": isAcademicYear})    
                except DoesNotExist:
                    pass

    print("FINAL DATA:", celtsLabor)            
    if celtsLabor:
        CeltsLabor.insert_many(celtsLabor).on_conflict_ignore().execute()
    print("FINAL DATA:", celtsLabor)
    
def getCeltsLaborHistory(volunteer):
    
    laborHistoryList = list(CeltsLabor.select(CeltsLabor.positionTitle, 
                                              Term.description, 
                                              Term.academicYear, 
                                              Term.isSummer)
                                      .join(Term, on=(CeltsLabor.term == Term.id))
                                      .where(CeltsLabor.user == volunteer))
    
    laborHistoryDict= {}
    for position in laborHistoryList: 
        laborHistoryDict[position.positionTitle] = position.term.description if position.term.isSummer else position.term.academicYear

    return laborHistoryDict