import pytest 

from app.models.user import User
from app.logic.celtsLabor import getPositionAndTerm
from app.logic import celtsLabor

def demoCallLsfApi(bnumber): 
    fakeLsfData = {"B00751864":[{"positionTitle": "Fake Position",
                                 "termCode": "202000",
                                 "laborStart": 12-13-2020,
                                 "laborEnd": 12-13-2021,
                                 "jobType": "Primary", 
                                 "wls": "1", 
                                 "termName": "AY 2020-2021"},
                                 {"positionTitle": "Fake Position",
                                 "termCode": "202000",
                                 "laborStart": 12-13-2021,
                                 "laborEnd": 12-13-2022,
                                 "jobType": "Primary", 
                                 "wls": "1", 
                                 "termName": "AY 2021-2022"},
                                 {"positionTitle": "Fake Position But a Leader",
                                 "termCode": "202000",
                                 "laborStart": 12-13-2022,
                                 "laborEnd": 12-13-2023,
                                 "jobType": "Primary", 
                                 "wls": "1", 
                                 "termName": "AY 2022-2023"},
                                 {"positionTitle": "Fake Position In The Summer",
                                 "termCode": "202013",
                                 "laborStart": 12-13-2021,
                                 "laborEnd": 12-13-2022,
                                 "jobType": "Primary", 
                                 "wls": "1", 
                                 "termName": "AY 2021-2022"},
                                 {"positionTitle": "Fake Position Not In AY or Summer",
                                 "termCode": "202004",
                                 "laborStart": 12-13-2021,
                                 "laborEnd": 12-13-2022,
                                 "jobType": "Primary", 
                                 "wls": "1", 
                                 "termName": "AY 2021-2022"},]
                                }
    return fakeLsfData

celtsLabor.getStudentFromLsf = demoCallLsfApi

@pytest.mark.integration
def test_getPositionAndTerm():
    volunteer = User.get(User.username == "neillz")
    neillzPositionAndTermInfo = getPositionAndTerm(volunteer)

    assert neillzPositionAndTermInfo == {'Fake Position': ['AY 2020-2021', 'AY 2021-2022'], 
                                         'Fake Position But a Leader': ["AY 2022-2023"],
                                         'Fake Position In The Summer': ['AY 2021-2022']}
