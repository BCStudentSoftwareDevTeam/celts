import pytest
from peewee import DoesNotExist

from app.models import mainDB
from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement

from app.logic.certification import getCertRequirements, updateCertRequirements

@pytest.mark.integration
def test_getCertRequirements():
    allreqs = getCertRequirements()

    certNames =  ["Bonner", "CESC Minor", "CPR", "Confidentiality", "I9"]
    assert certNames == [cert["data"].name for (id, cert) in allreqs.items()]

    cprReqs = allreqs[3]['requirements']
    assert ["Volunteer Training", "CPR Training"] == [r.name for r in cprReqs]

    cescreqs = getCertRequirements(certification=Certification.CESC)
    bonnerreqs = getCertRequirements(certification=Certification.BONNER)
    assert len(bonnerreqs) == 9

    nonereqs = getCertRequirements(certification=1111)
    assert len(nonereqs) == 0

@pytest.mark.integration
def test_updateCertRequirements():

    with mainDB.atomic() as transaction:

        cprcert = 3
        othercert = 4

        # Removal of missing items
        returnedIds = updateCertRequirements(cprcert, [])
        selectedIds = getCertRequirements(certification=cprcert)
        
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
        returnedIds = updateCertRequirements(cprcert, newRequirements)
        selectedIds = getCertRequirements(certification=cprcert)
        
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
        returnedIds = updateCertRequirements(othercert, newRequirements)
        selectedIds = getCertRequirements(certification=othercert)
        
        assert selectedIds == list(CertificationRequirement.select().where(CertificationRequirement.certification == othercert).order_by(CertificationRequirement.order))
        assert returnedIds == selectedIds
        assert returnedIds[1].name == "CPR 2"
        assert returnedIds[1].frequency == "once"
        assert returnedIds[1].isRequired == False

        transaction.rollback()

