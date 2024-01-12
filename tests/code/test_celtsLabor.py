import pytest

from app.models import mainDB
from app.models.user import User
from app.models.celtsLabor import CeltsLabor
from app.models.term import Term

from app.logic.celtsLabor import updateCeltsLaborFromLsf, collapsePositions, refreshCeltsLaborRecords, getCeltsLaborHistory
from app.logic import celtsLabor

@pytest.mark.integration
def test_collapsePositions():
    positionList = [{'positionTitle': 'Fake Position', 
                     'termCode': '202000', 
                     'laborStart': -2021, 
                     'laborEnd': -2022, 
                     'jobType': 'Primary', 
                     'wls': '1', 
                     'termName': 'AY 2020-2021'}, 
                    {'positionTitle': 'Fake Position', 
                     'termCode': '202000', 
                     'laborStart': -2022, 
                     'laborEnd': -2023, 
                     'jobType': 'Primary', 
                     'wls': '1', 
                     'termName': 'AY 2021-2022'}, 
                    {'positionTitle': 'Fake Position But a Leader', 
                     'termCode': '202000', 
                     'laborStart': -2023, 
                     'laborEnd': -2024, 
                     'jobType': 'Primary', 
                     'wls': '1', 
                     'termName': 'AY 2022-2023'},
                    {"positionTitle": "Fake Position In The Summer",
                     "termCode": "202013",
                     "laborStart": 12-13-2021,
                     "laborEnd": 12-13-2022,
                     "jobType": "Primary", 
                     "wls": "1", 
                     "termName": "AY 2021-2022"}]

    collapsed = collapsePositions(positionList)
    assert collapsed == {'Fake Position': ['2020-2021', '2021-2022'], 
                         'Fake Position But a Leader': ['2022-2023'], 
                         'Fake Position In The Summer': ['2021-2022']}

@pytest.mark.integration
def test_refreshCeltsLaborRecords():
    '''
    Assert that the CeltsLabor table contains what we expect. 

    Assert that records passed in throught laborDict are added as expect. 
    
    Assert that the original record for ayisie is deleted and the new record 
    from laborDict is now in the table. 
    '''
    
    laborDict = {"neillz": {'Fake Position': ['2020-2021', '2021-2022'], 
                            'Fake Position But a Leader': ['2022-2023'], 
                            'Fake Position In The Summer': ['2021-2022']
                           },
                 "ayisie": {'Not Bonner Manager': ['2020-2021']}
                }
    celtsLaborBase = [row.user for row in CeltsLabor.select()]
    
    mupotsal = User.get_by_id('mupotsal')
    ayisie = User.get_by_id('ayisie')
    neillz = User.get_by_id('neillz')

    summer2021 = Term.get_by_id(3)
    assert ayisie  in celtsLaborBase 
    assert mupotsal in celtsLaborBase 
    assert neillz not in celtsLaborBase
    ayisieBasePosition = list(CeltsLabor.select().where(CeltsLabor.user == "ayisie"))
    assert ayisieBasePosition[0].positionTitle == "Bonner Manager"
    assert ayisieBasePosition[0].term == summer2021
    assert ayisieBasePosition[0].isAcademicYear == False

    with mainDB.atomic() as transaction:
        refreshCeltsLaborRecords(laborDict)

        celtsLaborTest = [row.user for row in CeltsLabor.select()]
        assert ayisie  in celtsLaborTest 
        assert mupotsal in celtsLaborTest 
        assert neillz in celtsLaborTest

        # Check that the position record for ayisie in base data is no longer in the table but the new one that 
        # that was passed in with laborDict is. 
        Fall2020 = Term.get_by_id(1)
        ayisieNewPosition = list(CeltsLabor.select().where(CeltsLabor.user == "ayisie"))
        assert ayisieNewPosition[0].positionTitle == "Not Bonner Manager"
        assert ayisieNewPosition[0].term == Fall2020
        assert ayisieNewPosition[0].isAcademicYear == True
        assert "Bonner Manager" not in ayisieNewPosition

        transaction.rollback()
        
def demoLsfData(): 
    '''
    Mock up of the JSON resonse data that is returend from the LSF endpoint.
    '''
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
                                 "termName": "AY 2021-2022"}],
                   "B00751360":[{"positionTitle": "Fake Position Tyler",
                                 "termCode": "202000",
                                 "laborStart": 12-13-2020,
                                 "laborEnd": 12-13-2021,
                                 "jobType": "Primary", 
                                 "wls": "1", 
                                 "termName": "AY 2020-2021"}],
                   "B00759117":[{"positionTitle": "Fake Position Karina",
                                 "termCode": "202000",
                                 "laborStart": 12-13-2020,
                                 "laborEnd": 12-13-2021,
                                 "jobType": "Primary", 
                                 "wls": "1", 
                                 "termName": "AY 2020-2021"}]
                                }
    return fakeLsfData

# Tell getCeltsLaborFromLsf to use demoLsfData instead of trying to actually hit the LSF endpoint.
celtsLabor.getCeltsLaborFromLsf = demoLsfData

@pytest.mark.integration
def test_updateCeltsLaborFromLsf():
    '''
    Assert that the CeltsLabor table contains what we expect. 
    
    Call the function and assert that the records that were supossed to be added were 
    and that the records that were already in the table are also still there. 
    '''
    celtsLaborBase = [row.user for row in CeltsLabor.select()]
    
    mupotsal = User.get_by_id('mupotsal')
    ayisie = User.get_by_id('ayisie')
    neillz = User.get_by_id('neillz')
    agliullovak = User.get_by_id('agliullovak')
    partont = User.get_by_id('partont')

    assert ayisie  in celtsLaborBase 
    assert mupotsal in celtsLaborBase 
    assert neillz not in celtsLaborBase
    assert agliullovak not in celtsLaborBase
    assert partont not in celtsLaborBase

    with mainDB.atomic() as transaction: 
        updateCeltsLaborFromLsf()    
        Fall2020 = Term.get_by_id(1)
        Fall2024 = Term.get_by_id(4)
        celtsLaborTest = [row.user for row in CeltsLabor.select()]
        
        assert agliullovak in celtsLaborTest
        assert partont in celtsLaborTest
        assert neillz in celtsLaborTest
        assert ayisie  in celtsLaborTest 
        assert mupotsal in celtsLaborTest

        newZachPositions = list(CeltsLabor.select().where(CeltsLabor.user == "neillz"))
        
        assert newZachPositions[0].positionTitle == "Fake Position"
        assert newZachPositions[0].term == Fall2020
        assert newZachPositions[0].isAcademicYear == True
        assert newZachPositions[1].positionTitle == "Fake Position"
        assert newZachPositions[1].term == Fall2024
        assert newZachPositions[1].isAcademicYear == True
        # Check that "Fake Position Not In AY or Summer" was not added to the table since it was not 
        # held in either of the terms we are wanting to record. 
        for position in newZachPositions:
            assert "Fake Position Not In AY or Summer" not in position.positionTitle

        transaction.rollback()

@pytest.mark.integration
def test_getCeltsLaborHistory():
    testDataAyisieHistory = {"Bonner Manager": "Summer 2021"}
    getAyisieHistory = getCeltsLaborHistory(User.get_by_id("ayisie"))

    testDataMupotsalHistory = {"Habitat For Humanity Cord.": "2020-2021"}
    getMupotsalHistory = getCeltsLaborHistory(User.get_by_id("mupotsal"))

    assert getAyisieHistory == testDataAyisieHistory
    assert getMupotsalHistory == testDataMupotsalHistory