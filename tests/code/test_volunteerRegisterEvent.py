import pytest
from app.models.user import User
from app.controllers.events.volunteerRegisterEvent import volunteerRegister
from app.models.event import Event
from peewee import DoesNotExist

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
        volunteer = volunteerRegister("khatts", 15)

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts", "Event")

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts", -1)

    with pytest.raises(DoesNotExist):
        volunteer = volunteerRegister("khatts", 0)

@pytest.mark.integration
def test_volunteerRegister():
    #try:

    volunteer = volunteerRegister("khatts", 1)
    assert volunteer.user.username == "khatts"
    assert volunteer.event.id == 1
    assert volunteer.rsvp == True
