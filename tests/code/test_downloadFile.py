import pytest


from app import app
from app.logic.courseManagement import approvedCourses
from app.logic.downloadFile import fileMaker
from app.models.course import Course
from app.models import mainDB

designator = "downloadApprovedCourses"
csvInfo = approvedCourses(4)
fileFormat = {"headers":["Course Name", "Course Number", "Faculty", "Term"]}

@pytest.mark.integration
def test_makeFile():
    with app.app_context():
        with mainDB.atomic() as transaction:
            updateCourses = (Course.update({Course.status_id : 3, Course.term_id: 4}).where(Course.status_id != 3))
            updateCourses.execute()
            newFile = fileMaker(designator, csvInfo, "CSV", fileFormat)
            transaction.rollback()
            assert "File Downloaded Created Successfully"
