from copy import copy
from app.models.course import Course
from app.models.user import User
from app.models.term import Term
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.note import Note

def getServiceLearningCoursesData(user):
    """Returns dictionary with data used to populate Service-Learning proposal table"""
    courses = (Course.select()
                     .where(CourseInstructor.user==user)
                     .join(CourseInstructor)
                     .order_by(Course.id))
    courseDict = {}
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

def withdrawProposal(courseID):
    """Withdraws proposal of ID passed in. Removes foreign keys first.
    Key Dependencies: QuestionNote, CourseQuestion, CourseParticipant,
    CourseInstructor, Note"""
    course = Course.get(Course.id == courseID)
    questions = CourseQuestion.select().where(CourseQuestion.course == course)
    notes = list(Note.select(Note.id)
                .where(QuestionNote.question
                .in_(questions))
                .distinct()
                .join(QuestionNote))
    course.delete_instance(recursive=True)
    for note in notes:
        note.delete_instance()

def renewProposal(courseID, term):
    course = Course.get(Course.id == courseID)
    oldTerm = course.term
    course.id = None
    course.status = 1
    course.term = Term.get_by_id(term)
    course.save()
    oldCourse = Course.get(courseName=course.courseName, term=oldTerm)
    questions = list(CourseQuestion.select()
                    .join(Course)
                    .where(CourseQuestion.course==oldCourse.id,
                    Course.term==oldTerm,
                    Course.courseName==course.courseName))
    for question in questions:
        CourseQuestion.create(course=course.id,
                              questionContent=question.questionContent,
                              questionNumber=question.questionNumber)
    instructors = list(CourseInstructor.select()
                      .join(Course)
                      .where(CourseInstructor.course==oldCourse.id,
                      Course.term==oldTerm,
                      Course.courseName==course.courseName))
    for instructor in instructors:
        CourseInstructor.create(course=course.id,
                                user=instructor.user)
