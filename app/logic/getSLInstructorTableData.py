from flask import Flask, g
from app.models.course import Course
from app.models.user import User
from app.models.courseInstructor import CourseInstructor

def getProposalData():
    """Returns dictionary with data used to populate SL proposal table"""
    courses = (Course.select()
                     .where(CourseInstructor.user==g.current_user)
                     .join(CourseInstructor))
    courseDict = {}
    for course in courses:
        courseDict[course.courseName] = {
        "name":course.courseName,
        "faculty":0,
        "term":course.term.description,
        "status":course.status.status}
    return courseDict
