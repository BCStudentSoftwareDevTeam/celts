import pytest
from peewee import DoesNotExist

from app.models import mainDB
from app.models.certification import Certification

from app.logic.certification import getCertRequirements

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
