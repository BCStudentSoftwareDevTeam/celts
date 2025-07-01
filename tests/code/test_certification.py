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

    certNames = ["Bonner", "CCE Minor", "CPR", "Confidentiality", "I9"]
    # Ensure allRequirements has the expected keys and structure
    assert certNames == [cert["data"].name for cert in allRequirements.values() if "data" in cert and hasattr(cert["data"], "name")]
    # Use .get to avoid KeyError if 3 is not present
    cpr = allRequirements.get(3, {}).get('requirements', [])
    assert ["Volunteer Training", "CPR Training"] == [r.name for r in cpr]

    bonner = getCertRequirements(certification=getattr(Certification, "BONNER", None))
    assert isinstance(bonner, list)
    assert len(bonner) == 9

    noRequirements = getCertRequirements(certification=1111)
    assert isinstance(noRequirements, list)
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

