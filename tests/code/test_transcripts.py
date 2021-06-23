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
def test_getTranscripts():
    user = User.get_by_id("neillz")
    transcript = getSLCourseTranscript(user)
    assert transcript[0] == ["Databases", "Spring B 2021", ["Zach Neill"], 2.0]
    assert transcript[1] == ["Spanish Help", "Spring A 2021", ["Zach Neill","Brian Ramsay"], 3.0]
    transcript = getProgramTranscript(user)
    assert transcript[0] == ["Training", "Fall 2021", 3.0]
    assert transcript[1] == ["Adopt A Grandparent", "Summer 2021", 3.0]
    assert transcript[2] == ["Berea Buddies", "Spring B 2021", 1.0]
