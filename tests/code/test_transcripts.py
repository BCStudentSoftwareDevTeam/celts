import pytest
from peewee import DoesNotExist

from app.controllers.events.view_transcript import getSLCourseTranscript
from app.controllers.events.view_transcript import getProgramTranscript
# from app.controllers.events.view_transcript import getUser
from app.models.term import Term
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.user import User
from app.models.eventParticipant import EventParticipant

# @pytest.mark.integration
# def test_noGetSLTranscript():
#
#     with pytest.raises(DoesNotExist):
#         sLcourse = getSLCourseTranscript(User.get_by_id("ggiuo"))
#     with pytest.raises(DoesNotExist):
#         sLcourse = getSLCourseTranscript(User.get_by_id(69809))
#
# @pytest.mark.integration
# def test_noGetProgramTranscript():
#
#     with pytest.raises(DoesNotExist):
#         sLcourse = getProgramTranscript(User.get_by_id("adfafa"))
#     with pytest.raises(DoesNotExist):
#         sLcourse = getProgramTranscript(User.get_by_id(56498))

# @pytest.mark.integration
# def test_noGetUser():
#
#     with pytest.raises(DoesNotExist):
#         sLcourse = getUser(User.get_by_id("vhvkj"))
#     with pytest.raises(DoesNotExist):
#         sLcourse = getUser(User.get_by_id(468598))


@pytest.mark.integration
def test_getSLTranscripts():
    user = User.get_by_id("neillz")
    # print(user)
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


@pytest.mark.integration
def test_getProgramTranscripts():

    user = User.get_by_id("neillz")
    transcript = getProgramTranscript(user)
    print(transcript, "Zach Transcript")
    # assert transcript[0] == ["Berea Buddies", "Fall 2021", 4.0]
    # assert transcript[1] == ["Adopt A Grandparent", "Summer 2021", 3.0]
    # assert transcript[3] == ["Empty Bowls", "Sping A 2021", 20.0]

    # user = User.get_by_id("ramsayb2")
    # transcript = getProgramTranscript(user)
    # assert transcript[0] == ["Training", "Fall 2021", 4.0]
    # assert transcript[1] == ["Adopt A Grandparent", "Summer 2021", 2.0]

    # user = User.get_by_id("khatts")
    # transcript = getProgramTranscript(user)
    # print(transcript, "Sreynit Transcript")

# @pytest.mark.integration
# def test_getUser():
#     user = User.get_by_id("neillz")
#     name = getUser(user)
#     assert name == "Zach Neill"
