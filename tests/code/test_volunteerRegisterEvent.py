import pytest
from app.models.user import User
from app.controllers.events.volunteerRegisterEvent import volunteerRegister
from app.models.event import Event

@pytest.mark.integration
def test_volunteerRegister():
    with pytest.raises(ValueError):
        raise ValueError("requirements not met")

    # with pytest.raises(ValueError, match=r".* incorrect values.*"):
    #     raise ValueError("You put in incorrect values")

    user = User.get(User.username == "khatts")
    event = Event.get(Event.id == 1)


    volunteer = volunteerRegister(user, event)

    assert volunteer.user.username == "khatts"
    assert volunteer.event.id == 1
    assert volunteer.rsvp == True
