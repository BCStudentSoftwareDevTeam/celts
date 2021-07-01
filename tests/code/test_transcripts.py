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
        sLcourse = getSLCourseTranscript(User.get_by_id("ggiuo"))
    with pytest.raises(DoesNotExist):
        sLcourse = getSLCourseTranscript(User.get_by_id(69809))

@pytest.mark.integration
def test_noGetProgramTranscript():

    with pytest.raises(DoesNotExist):
        sLcourse = getProgramTranscript(User.get_by_id("adfafa"))
    with pytest.raises(DoesNotExist):
        sLcourse = getProgramTranscript(User.get_by_id(56498))

@pytest.mark.integration
def test_getSLTranscripts():
    user = User.get_by_id("neillz")
    transcript = getSLCourseTranscript(user)

    assert transcript[0][0]['fullName'] == ["Zach Neill"]
    assert transcript[0][1]['courseName'] == "Databases"
    assert transcript[0][2]['termName'] == "Spring B 2021"
    assert transcript[0][3]['cHoursAccrued'] == 2.0
    assert transcript[0][4]['cInstructorName'] == ["Brian Ramsay"]

    assert transcript[1][0]['fullName'] == ["Zach Neill"]
    assert transcript[1][1]['courseName'] == "Spanish Help"
    assert transcript[1][2]['termName'] == "Spring A 2021"
    assert transcript[1][3]['cHoursAccrued'] == 3.0
    assert transcript[1][4]['cInstructorName'] == ["Brian Ramsay"]

    # User that attends a course multiple times
    # We still need to decide whether we want to create multiple entries for the same course or just update
    # the hoursEarned.
    user2 = User.get_by_id("khatts")
    transcript2 = getSLCourseTranscript(user2)

    assert transcript2[0][0]['fullName'] == ["Sreynit Khatt"]
    assert transcript2[0][1]['courseName'] == "Spanish Help"
    assert transcript2[0][2]['termName'] == "Spring A 2021"
    assert transcript2[0][3]['cHoursAccrued'] == 8.0
    assert transcript2[0][4]['cInstructorName'] == ["Brian Ramsay"]

    assert transcript2[1][0]['fullName'] == ["Sreynit Khatt"]
    assert transcript2[1][1]['courseName'] == "Databases"
    assert transcript2[1][2]['termName'] == "Spring B 2021"
    assert transcript2[1][3]['cHoursAccrued'] == 1.0
    assert transcript2[1][4]['cInstructorName'] == ["Brian Ramsay"]

@pytest.mark.integration
def test_getProgramTranscripts():

    user = User.get_by_id("neillz")
    transcript = getProgramTranscript(user)
    assert transcript[0] == ['Berea Buddies', 'Spring A 2021', 4.0]
    assert transcript[1] == ['Adopt A Grandparent', 'Summer 2021', 3.0]
    assert transcript[2] == ['Empty Bowls', 'Spring A 2021', 8.0]


    user = User.get_by_id("khatts")
    transcript = getProgramTranscript(user)
    assert transcript[0] == ['Empty Bowls', 'Spring A 2021', 3.0]
    assert transcript[1] == ['Berea Buddies', 'Spring A 2021', 10.0] #Program that has events from different term.
