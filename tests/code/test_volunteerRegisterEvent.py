import pytest
from app.models.user import User
from app.controllers.events.volunteerRegisterEvent import volunteerRegister
from app.models.event import Event
from peewee import DoesNotExist
from app.controllers.events.meetsReqsForEvent import isEligibleForProgram

@pytest.mark.integration
def test_noUserVolunteerRegister():

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("asdkl", 1)

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister(132546, 1)

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister(" khatts", 1)

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts ", 1)

@pytest.mark.integration
def test_noEventVolunteerRegister():

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts", 1500)

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts", "Event")

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts", -1)

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts", 0)


@pytest.mark.integration
def test_volunteerRegister():

    volunteer = volunteerRegister("lamichhanes2", 2)

    print(volunteer)

    assert volunteer.user.username == "lamichhanes2"
    assert volunteer.event.id == 2
    assert volunteer.rsvp == True
