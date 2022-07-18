from app.models.course import Course
from app.models.user import User
from app.models.term import Term
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.courseStatus import CourseStatus
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.note import Note
from app.models.term import Term


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
        otherInstructors = (CourseInstructor.select(CourseInstructor, User).join(User).where(CourseInstructor.course==course))
        faculty = [f"{instructor.user.firstName} {instructor.user.lastName}" for instructor in otherInstructors]
        courseDict[course.id] = {
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
                .join(QuestionNote)
                .where(QuestionNote.question.in_(questions))
                .distinct())
    course.delete_instance(recursive=True)
    for note in notes:
        note.delete_instance()

def renewProposal(courseID, term):
    course = Course.get(Course.id == courseID)
    oldTerm = course.term
    course.id = None
    course.term = Term.get_by_id(term)
    oldCourse = Course.get(courseName=course.courseName, term=oldTerm)
    oldCourse.status=course.status
    course.status = 3
    course.save()
    oldCourse.save()
    questions = (CourseQuestion.select(CourseQuestion, Course)
                    .join(Course)
                    .where(CourseQuestion.course==oldCourse.id,
                    Course.term==oldTerm,
                    Course.courseName==course.courseName))
    for question in questions:
        CourseQuestion.create(course=course.id,
                              questionContent=question.questionContent,
                              questionNumber=question.questionNumber)
    instructors = (CourseInstructor.select()
                                   .where(CourseInstructor.course==oldCourse.id))
    for instructor in instructors:
        CourseInstructor.create(course=course.id,
                                user=instructor.user)
