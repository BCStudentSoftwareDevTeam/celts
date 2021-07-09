import pytest
from app.models.user import User
from app.controllers.events.volunteerRegisterEvent import volunteerRegister
from app.models.event import Event
from peewee import DoesNotExist
from app.controllers.events.programEligibility import isEligibleForProgram

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

    volunteer = volunteerRegister("lamichhanes2", 10)

    print(volunteer)
    assert volunteer.user.username == "lamichhanes2"
    assert volunteer.event.id == 10
    assert volunteer.rsvp == True

    # the user has already registered for the event
    volunteer2 = volunteerRegister("lamichhanes2", 10)
    assert volunteer2
<<<<<<< HEAD
    print(volunteer2)

    # the user is not eligible to register
    volunteer3 = volunteerRegister("ayisie", 7)
    print(volunteer3)
=======

    # the user is not eligible to register
    volunteer3 = volunteerRegister("ayisie", 7)
>>>>>>> 83dbdbc4d62baefba4dee3c710c9ce9609c39db3
    assert volunteer3
