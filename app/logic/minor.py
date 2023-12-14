from app.models.user import User
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.models.program import Program
from app.models.event import Event
from app.models.courseInstructor import CourseInstructor
from app.models.eventParticipant import EventParticipant
from collections import defaultdict
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn

def updateMinorInterest(username):
    """
    Given a username, update their minor interest and minor status.
    """
    user = User.get(username=username)
    user.minorInterest = not user.minorInterest
    if user.minorInterest == True:
        user.minorStatus = "Interested"
    else:
        user.minorStatus = "No interest"

    user.save()

def getCourseInformation(id):
    """
        Given a course ID, return an object containing the course information and 
        its instructors full names.
    """

    # retrieve the course and the course instructors
    course = model_to_dict(Course.get_by_id(id))

    courseInstructors = (CourseInstructor.select(CourseInstructor, User)
                                         .join(Course).switch()
                                         .join(User)
                                         .where(Course.id == id))
    
    courseInformation = {"instructors": [(instructor.user.firstName + " " + instructor.user.lastName) for instructor in courseInstructors], "course": course}

    return courseInformation

def getProgramEngagementHistory(program_id, username, term_id):
    """
        Given a program_id, username, and term_id, return an object containing all events in the provided program 
        and in the given term along with the program name.
    """

    # execute a query that will retrieve all events in which the user has participated
    # that fall under the provided term and programs.
    eventsInProgramAndTerm = (Event.select(Event.id, Event.name, fn.SUM(EventParticipant.hoursEarned).alias("hoursEarned"))
                                   .join(Program).switch()
                                   .join(EventParticipant)
                                   .where(EventParticipant.user == username,
                                          Event.term == term_id,
                                          Program.id == program_id)
                             )
    
    program = Program.get_by_id(program_id)

    # calculate total amount of hours for the whole program that term
    totalHours = 0
    for event in eventsInProgramAndTerm:
        if event.hoursEarned:
            totalHours += event.hoursEarned
    
    participatedEvents = {"program":program.programName, "events": [event for event in eventsInProgramAndTerm.dicts()], "totalHours": totalHours}

    return participatedEvents



def getCommunityEngagementByTerm(username):
    """
    Given a username, return all of their community engagements (service learning courses and event participations.)
    """
    courses = (Course.select(Course)
                     .join(CourseParticipant, on=(Course.id == CourseParticipant.course))
                     .where(CourseParticipant.user == username)
                     .group_by(Course.courseName, Course.term))
    
    # initialize default dict to store term descriptions as keys mapping to each
    # engagement's respective type, name, id, and term.
    terms = defaultdict(list)
    for course in courses:
        terms[(course.term.description, course.term.id)].append({"name":course.courseName, "id":course.id, "type":"course", "term":course.term})

    events = (Event.select(Event, Program)
                   .join(EventParticipant, on=(Event.id == EventParticipant.event)).switch()
                   .join(Program)
                   .where(EventParticipant.user == username)
                   .group_by(Event.program, Event.term))
    
    for event in events:
        terms[(event.term.description, event.term.id)].append({"name":event.program.programName, "id":event.program.id, "type":"program", "term":event.term})
    
    # sorting the terms by the term id
    return dict(sorted(terms.items(), key=lambda x: x[0][1]))



