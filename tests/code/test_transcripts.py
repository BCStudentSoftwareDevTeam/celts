import pytest
from peewee import DoesNotExist

from app.controllers.events.view_transcript import getSLCourseTranscript

from app.models.term import Term
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.user import User



@pytest.mark.integration
def test_getCourseTranscript():

    user = User.get_by_id("neillz")
    transcript = getSLCourseTranscript(user)
    assert transcript[0] == ["Databases", "Spring B 2021", ["Zach Neill"], "2"]
    assert transcript[1] == ["Spanish Help", "Spring A 2021", ["Zach Neill","Brian Ramsay"], "3"]
