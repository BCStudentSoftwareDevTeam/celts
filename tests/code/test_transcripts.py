import pytest
from peewee import DoesNotExist

from app.controllers.events.view_transcript import getSLCourseTranscript
from app.controllers.events.view_transcript import getProgramTranscript
from app.models.term import Term
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.user import User
from app.models.eventParticipant import EventParticipant

@pytest.mark.integration
def test_noGetSLTranscript():

    with pytest.raises(DoesNotExist):
        sLcourse = getSLCourseTranscript("ggiuo")
    with pytest.raises(DoesNotExist):
        sLcourse = getSLCourseTranscript(69809)


@pytest.mark.integration
def test_noGetProgramTranscript():

    with pytest.raises(DoesNotExist):
        sLcourse = getProgramTranscript("adfafa")
    with pytest.raises(DoesNotExist):
        sLcourse = getProgramTranscript(56498)

@pytest.mark.integration
def test_getSLTranscripts():
    user = "neillz"
    transcript = getSLCourseTranscript(user)
    assert transcript[0] == ["Zach Neill", "Databases", "Spring B 2021", 2.0, ["Brian Ramsay"]]
    assert transcript[1] == ["Zach Neill", "Spanish Help", "Spring A 2021", 3.0, ["Brian Ramsay"]]

    # We still need to decide whether we want to create multiple entries for the same course or just update the hoursEarned.

    user2 = "khatts"  # User that attends a course multiple times
    transcript2 = getSLCourseTranscript(user2)
    assert transcript2[0] == ["Sreynit Khatt", "Spanish Help", "Spring A 2021", 8.0, ["Brian Ramsay"]]
    assert transcript2[1] == ["Sreynit Khatt", "Databases", "Spring B 2021", 1.0, ["Brian Ramsay"]]


@pytest.mark.integration
def test_getProgramTranscripts():

    user = User.get_by_id("neillz")
    transcript = getProgramTranscript(user)
    assert transcript[0] == ['Berea Buddies', 'Spring A 2021', 4.0]
    assert transcript[1] == ['Adopt A Grandparent', 'Summer 2021', 3.0]
    assert transcript[2] == ['Empty Bowls', 'Spring A 2021', 8.0]


    user2 = User.get_by_id("khatts")
    transcript2 = getProgramTranscript(user2)
    assert transcript2[0] == ['Empty Bowls', 'Spring A 2021', 3.0]
    assert transcript2[1] == ['Berea Buddies', 'Spring A 2021', 10.0] #Program that has events from different term.
