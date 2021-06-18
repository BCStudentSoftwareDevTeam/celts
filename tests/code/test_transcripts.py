import pytest
from peewee import DoesNotExist

from app.controllers.events.view_transcript import ViewCourseTranscript

from app.models.term import Term
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant


@pytest.mark.integration
def test_viewCourseTranscript():
    Course.courseName = 2
    Course.term = 2
    CourseParticipant.hoursEarned = 2
    transcript = ViewCourseTranscript()
    assert transcript
    # assert transcript[0].pName == "Empty Bowls"
    # assert transcript[1].pName == "Berea Buddies"
