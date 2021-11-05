from app.models.course import Course
from app.models.user import User
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from flask import g

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

def deleteProposal(courseID):
    """Deletes proposal of ID passed in. Removes foreign keys first.
    Key Dependencies: QuestionNote, CourseQuestion, CourseParticipant,
    CourseInstructor"""
    course = Course.get(Course.id == courseID)
    notes = (QuestionNote.select()
                         .where(CourseQuestion.course == course)
                         .join(CourseQuestion))
    if notes:
        for note in notes:
            note.delete_instance()
    (CourseQuestion.delete().where(CourseQuestion.course == course)).execute()
    (CourseParticipant.delete().where(CourseParticipant.course == course)).execute()
    (CourseInstructor.delete().where(CourseInstructor.course == course)).execute()
    course.delete_instance()

def authorized(username):
    if g.current_user.isAdmin or g.current_user.isFaculty:
        user = User.get(User.username == username)
        print(user)
        if user.isAdmin or user.isFaculty:
            return True
        else:
            return False
    else:
        return False
