import pytest
from app.logic.trackVolunteerHours import trackVolunteerHours

@pytest.mark.integration
def test_trackVolunteerHours():
    trackHours = trackVolunteerHours()
    print(list(trackHours))
    print(trackHours[7].user.firstName)
    # print(trackHours[7].event.)

    assert trackHours
