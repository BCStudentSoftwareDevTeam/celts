import pytest
from peewee import DoesNotExist

from app.models import mainDB
from app.models.event import Event
from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement
from app.models.requirementMatch import RequirementMatch
from app.models.eventParticipant import EventParticipant

from app.logic.certification import getCertRequirements, updateCertRequirements, updateCertRequirementForEvent
from app.logic.certification import getCertRequirementsWithCompletion

@pytest.mark.integration
def test_getCertRequirements():
    allRequirements = getCertRequirements()

    certNames =  ["Bonner", "CESC Minor", "CPR", "Confidentiality", "I9"]
    assert certNames == [cert["data"].name for (id, cert) in allRequirements.items()]

    cpr = allRequirements[3]['requirements']
    assert ["Volunteer Training", "CPR Training"] == [r.name for r in cpr]

    cesc = getCertRequirements(certification=Certification.CESC)
    bonner = getCertRequirements(certification=Certification.BONNER)
    assert len(bonner) == 9

    noRequirements = getCertRequirements(certification=1111)
    assert len(noRequirements) == 0

@pytest.mark.integration
def test_getCertRequirementsWithCompletion():

    with mainDB.atomic() as transaction:
        # add two matches for the same requirement to make sure we only return one row per requirement
        RequirementMatch.create(event_id=14, requirement_id=10)
        EventParticipant.create(event_id=14, user_id='ramsayb2')
        RequirementMatch.create(event_id=13, requirement_id=10)
        EventParticipant.create(event_id=13, user_id='ramsayb2')
        cprcert = 3

        cprreqs = getCertRequirementsWithCompletion(certification=cprcert, username='ramsayb2')
        assert len(cprreqs) == 2
        assert not cprreqs[0].completed, "The first event should not be completed"
        assert cprreqs[1].completed, "The second event should be completed"

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
        
        assert selectedIds == list(CertificationRequirement.select().where(CertificationRequirement.certification == otherId).order_by(CertificationRequirement.order))
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

