from app.models.course import Course
from app.models.user import User
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.note import Note
from app.models.term import Term
from app.models.courseStatus import CourseStatus

def getServiceLearningCoursesData(user):
    """Returns dictionary with data used to populate Service-Learning proposal table"""
    courses = (Course.select(Course, Term, CourseStatus)
                     .join(CourseInstructor).switch()
                     .join(Term).switch()
                     .join(CourseStatus)
                     .where(CourseInstructor.user==user)
                     .order_by(Course.id))

    courseDict = {}
    for course in courses:
        otherInstructors = CourseInstructor.select(CourseInstructor, User).join(User).where(CourseInstructor.course==course)
        faculty = [f"{instructor.user.firstName} {instructor.user.lastName}" for instructor in otherInstructors]
        courseDict[course.courseName] = {
        "id": course.id,
        "name": course.courseName,
        "faculty": faculty,
        "term": course.term,
        "status": course.status.status}
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
        note.delete_instance(recursive=True)
