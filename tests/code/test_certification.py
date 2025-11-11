import pytest
from flask import g
from peewee import DoesNotExist
from app import app
from app.models import mainDB
from app.models.event import Event
from app.models.term import Term
from app.models.user import User
from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement
from app.models.requirementMatch import RequirementMatch
from app.models.eventParticipant import EventParticipant

from app.logic.certification import getCertRequirements, updateCertRequirements, updateCertRequirementForEvent, termsAttended, termsMissed, termsInTotal
from app.logic.certification import getCertRequirementsWithCompletion
from app.logic.loginManager import getCurrentTerm

@pytest.mark.integration
def test_termsAttended():

    with mainDB.atomic() as transaction:
        with app.app_context():
            attendedTerms = termsAttended()
            assert attendedTerms == None
        transaction.rollback()

    with mainDB.atomic() as transaction:
        # created the database and added the test data to test what terms are return from attendedTerms()
        with app.app_context():
            Term.update(isCurrentTerm=False).execute()
            Term.create(id = 1000, description = "Spring 2020", year = 2020, academicYear = 2019-2020, isSummer = False, isCurrentTerm = True, termOrder = 2020-1)
            Term.create(id = 1001, description = "Fall 2019", year = 2019, academicYear = 2019-2020, isSummer = False, isCurrentTerm = False, termOrder = 2019-3)
            g.current_term = getCurrentTerm() 
            Event.create(id = 1400, term_id = 1000, name = "Event 1", description = "Spring 2020", program_id = 5)
            Event.create(id = 1401, term_id = 1001, name = "Event 2", description = "Spring 2019", program_id = 5)
            User.create(username='zawn', rawClassLevel='Senior')  
            CertificationRequirement.create(id = 400, certification_id = 1, name = "CPR Training", frequency = "term", required = True)
            RequirementMatch.create(event_id=1400, requirement_id=400)
            EventParticipant.create(event_id=1400, user_id='zawn')
            RequirementMatch.create(event_id=1401, requirement_id=400)
            EventParticipant.create(event_id=1401, user_id='zawn')
            attendedTermsNum = len(termsAttended(certification=400, username='zawn'))
        assert attendedTermsNum == 2
        transaction.rollback()
            
@pytest.mark.integration
def test_termsMissed():
    # created the database and added the test data to test the maximum amount of terms a student can miss based on their class level
    with mainDB.atomic() as transaction:
        with app.app_context():
            missedTerms = termsMissed()
            assert missedTerms == None
        transaction.rollback()

    with mainDB.atomic() as transaction:
        with app.app_context():
            Term.update(isCurrentTerm=False).execute()
            Term.create(id = 1000, description = "Fall 2019", year = 2019, academicYear = 2019-2020, isSummer = False, isCurrentTerm = True, termOrder = 2019-3)
            g.current_term = getCurrentTerm() 
            Event.create(id = 1400, term_id = 1000, name = "Event 1", description = "Fall 2019", program_id = 5)
            User.create(username='zawn', rawClassLevel='Senior')  
            CertificationRequirement.create(id = 400, certification_id = 1, name = "CPR Training", frequency = "term", required = True)
            RequirementMatch.create(event_id=1400, requirement_id=400)
            EventParticipant.create(event_id=1400, user_id='zawn')
            missedTerms = termsMissed(certification=400, username='zawn')
        assert missedTerms == ['Fall 2016', 'Spring 2017', 'Fall 2017', 'Spring 2018', 'Fall 2018', 'Spring 2019'] 
        transaction.rollback()
    
    
    with mainDB.atomic() as transaction:
        with app.app_context():
            Term.update(isCurrentTerm=False).execute()
            Term.create(id = 1000, description = "Summer 2022", year = 2022, academicYear = 2022-2023, isSummer = True, isCurrentTerm = True, termOrder = 2022-2)
            g.current_term = getCurrentTerm() 
            Event.create(id = 1400, term_id = 1000, name = "Event 1", description = "Summer 2022", program_id = 5)
            User.create(username='zawn', rawClassLevel='Freshman')  
            CertificationRequirement.create(id = 400, certification_id = 1, name = "CPR Training", frequency = "term", required = True)
            missedTerms = termsMissed(certification=400, username='zawn')
        assert missedTerms == ["Fall 2022"]
        transaction.rollback()
     
    with mainDB.atomic() as transaction:
        with app.app_context():
            Term.update(isCurrentTerm=False).execute()
            Term.create(id = 1001, description = "Spring 2022", year = 2022, academicYear = 2021-2022, isSummer = False, isCurrentTerm = True, termOrder = 2022-1)
            Term.create(id = 1000, description = "Spring 2021", year = 2021, academicYear = 2020-2021, isSummer = False, isCurrentTerm = False, termOrder = 2021-1)
            g.current_term = getCurrentTerm() 
            Event.create(id = 1400, term_id = 1000, name = "Event 1", description = "Spring 2021", program_id = 5)
            User.create(username='zawn', rawClassLevel='Junior')  
            CertificationRequirement.create(id = 400, certification_id = 1, name = "CPR Training", frequency = "term", required = True)
            RequirementMatch.create(event_id=1400, requirement_id=400)
            EventParticipant.create(event_id=1400, user_id='zawn')
            missedTerms = termsMissed(certification=400, username='zawn')
        assert missedTerms == ["Fall 2019", "Spring 2020", "Fall 2020", "Fall 2021", "Spring 2022"]
        transaction.rollback()

@pytest.mark.integration
def test_termsInTotal():  
        
    with mainDB.atomic() as transaction:
        with app.app_context():
            totalTerms = termsInTotal()
            assert totalTerms == None
        transaction.rollback()

    with mainDB.atomic() as transaction:
        with app.app_context():
            Term.update(isCurrentTerm=False).execute()
            Term.create(id = 1000, description = "Spring 2021", year = 2021, academicYear = 2020-2021, isSummer = False, isCurrentTerm = True, termOrder = 2021-1)
            g.current_term = getCurrentTerm() 
            User.create(username='zawn', rawClassLevel='Senior') 
            totalTerms = termsInTotal(username='zawn')
            assert totalTerms == ["Fall 2017", "Spring 2018", "Fall 2018", "Spring 2019", "Fall 2019", "Spring 2020", "Fall 2020", "Spring 2021"]
        transaction.rollback()

    with mainDB.atomic() as transaction:
        with app.app_context():
            Term.update(isCurrentTerm=False).execute()
            Term.create(id = 1000, description = "Fall 2018", year = 2018, academicYear = 2017-2018, isSummer = False, isCurrentTerm = True, termOrder = 2018-3)
            g.current_term = getCurrentTerm() 
            User.create(username='zawn', rawClassLevel='Sophomore') 
            totalTerms = termsInTotal(username='zawn')
            assert totalTerms == ["Fall 2017", "Spring 2018", "Fall 2018"]
        transaction.rollback()


@pytest.mark.integration
def test_getCertRequirements():
        with mainDB.atomic() as transaction:
            allRequirements = getCertRequirements()

            certNames =  ["Bonner", "CCE Minor", "CPR", "Confidentiality", "I9"]
            assert certNames == [cert["data"].name for (id, cert) in allRequirements.items()]
            cpr = allRequirements[3]['requirements']
            assert ["Volunteer Training", "CPR Training"] == [r.name for r in cpr]

            bonner = getCertRequirements(certification=Certification.BONNER)
            assert len(bonner) == 9

            noRequirements = getCertRequirements(certification=1111)
            assert len(noRequirements) == 0
        transaction.rollback()



@pytest.mark.integration
def test_getCertRequirementsWithCompletion():

    with mainDB.atomic() as transaction:
        # add two matches for the same requirement to make sure we only return one row per requirement
        RequirementMatch.create(event_id=14, requirement_id=10)
        EventParticipant.create(event_id=14, user_id='ramsayb2')
        RequirementMatch.create(event_id=13, requirement_id=10)
        EventParticipant.create(event_id=13, user_id='ramsayb2')
        
        cprCert = 3
        cprReqs = getCertRequirementsWithCompletion(certification=cprCert, username='ramsayb2')
       
        assert len(cprReqs) == 2
        assert not cprReqs[0].completed, "The first event should not be marked as completed"
        assert cprReqs[1].completed, "The second event should be marked as completed"

        transaction.rollback()

@pytest.mark.integration
def test_updateCertRequirements():

    with mainDB.atomic() as transaction:

        cprId = 3
        otherId = 4

        # Removal of missing items
        returnedIds = updateCertRequirements(cprId, [])
        selectedIds = getCertRequirements(certification=cprId)

        assert returnedIds == []
        assert selectedIds == []

        transaction.rollback()

        # Update of existing items (with order change)
        newRequirements = [
                {'id': 10,
                 'name': 'CPR 1',
                 'frequency': 'annual',
                 'required': False},
                {'id': 11,
                 'name': 'CPR 2',
                 'frequency': 'term',
                 'required': False}
                ]
        returnedIds = updateCertRequirements(cprId, newRequirements)
        selectedIds = getCertRequirements(certification=cprId)
        
        assert selectedIds == [CertificationRequirement.get_by_id(10),CertificationRequirement.get_by_id(11)]
        assert returnedIds == selectedIds
        assert returnedIds[1].name == "CPR 2"
        assert returnedIds[1].frequency == "term"
        assert returnedIds[1].isRequired == False

        transaction.rollback()

        # Addition of new items
        newRequirements = [
                {'id': 'X',
                 'name': 'CPR 1',
                 'frequency': 'annual',
                 'required': False},
                {'id': 15,
                 'name': 'CPR 2',
                 'frequency': 'once',
                 'required': False}
                ]
        returnedIds = updateCertRequirements(otherId, newRequirements)
        selectedIds = getCertRequirements(certification=otherId)
        fetchedIds = list(CertificationRequirement.select().where(CertificationRequirement.certification == otherId).order_by(CertificationRequirement.order))
        
        assert selectedIds == fetchedIds
        assert returnedIds == selectedIds
        assert returnedIds[1].name == "CPR 2"
        assert returnedIds[1].frequency == "once"
        assert returnedIds[1].isRequired == False

        transaction.rollback()

@pytest.mark.integration
def test_updateCertRequirementForEvent():

    with mainDB.atomic() as transaction:
        RequirementMatch.create(event_id=14, requirement_id=8)

        # adding a requirement/event pair that already exists
        ev = Event.get_by_id(14)
        updateCertRequirementForEvent(ev, 8)
        results = RequirementMatch.select().where(RequirementMatch.requirement == 8)
        assert len(results) == 1

        # adding a requirement that is different for an existing event
        ev = Event.get_by_id(14)
        updateCertRequirementForEvent(ev, 9)
        results = RequirementMatch.select().where(RequirementMatch.event == ev)
        assert len(results) == 1, "Should have one requirement per event"

        # adding an event that is different for an existing requirement
        ev = Event.get_by_id(12)
        updateCertRequirementForEvent(ev, 9)
        results = RequirementMatch.select().where(RequirementMatch.event == ev)
        assert len(results) == 1, "Should have one requirement per event"
        results = RequirementMatch.select().where(RequirementMatch.requirement == 9)
        assert len(results) == 2, "Can have multiple events satisfying a requirement"


        # adding a new requirement/event pair
        transaction.rollback()
        ev = Event.get_by_id(14)
        updateCertRequirementForEvent(ev, 8)
        results = RequirementMatch.select().where(RequirementMatch.event == ev)
        assert len(results) == 1

        transaction.rollback()

