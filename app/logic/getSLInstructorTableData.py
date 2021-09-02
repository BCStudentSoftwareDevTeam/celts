from app.models.course import Course
from app.models.user import User
from app.models.courseInstructor import CourseInstructor

def getProposalData(user):
    """Returns dictionary with data used to populate SL proposal table"""
    courses = (Course.select()
                     .where(CourseInstructor.user==user)
                     .join(CourseInstructor)
                     .order_by(Course.id))
    courseDict = {} #a dictionary of dictionaries for better readability
    for course in courses:
        otherInstructors = (CourseInstructor.select().where(CourseInstructor.course==course))
        faculty = [f"{instructor.user.firstName} {instructor.user.lastName}" for instructor in otherInstructors]
        courseDict[course.courseName] = {
        "id":course.id,
        "name":course.courseName,
        "faculty": faculty,
        "term":course.term,
        "status":course.status.status}
    return courseDict
