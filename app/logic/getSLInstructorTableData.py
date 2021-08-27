from flask import Flask, g
from app.models.course import Course
from app.models.user import User
from app.models.courseInstructor import CourseInstructor

def getProposalData():
    """Returns dictionary with data used to populate SL proposal table"""
    courses = (Course.select()
                     .where(CourseInstructor.user==g.current_user)
                     .join(CourseInstructor))
    courseDict = {} #any reason why this is a dictionary of dictionaries, wouldn't a list of dictionaries be easier to work with?
    #I just thought it would be easier to read. But a list is a-ok too.
    for course in courses:
        otherInstructors = (CourseInstructor.select().where(CourseInstructor.course==course))
        faculty = [f"{instructor.user.firstName} {instructor.user.lastName}" for instructor in otherInstructors]
        courseDict[course.courseName] = {
        "name":course.courseName,
        "faculty": ', '.join(faculty),
        "term":course.term.description,
        "status":course.status.status}
    return courseDict
