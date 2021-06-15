import pytest
from peewee import DoesNotExist

from app.controllers.events.meetsReqsForEvent import isEligibleForProgram

@pytest.mark.integration
def test_is_eligible_for_program():
    # No program is given
    program_eligibility = isEligibleForProgram("Berea Buddies")
