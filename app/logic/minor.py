import re
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn, Case, DoesNotExist
from collections import defaultdict

from app.models.user import User
from app.models.event import Event
from app.models.course import Course
from app.models.program import Program
from app.models.certification import Certification
from app.models.courseInstructor import CourseInstructor
from app.models.eventParticipant import EventParticipant
from app.models.courseParticipant import CourseParticipant
from app.models.individualRequirement import IndividualRequirement
from app.models.certificationRequirement import CertificationRequirement
from app.models.communityEngagementRequest import CommunityEngagementRequest

def getMinorInterest():
    interestedStudents = (User.select(User.firstName, User.lastName, User.username)
                              .join(IndividualRequirement, JOIN.LEFT_OUTER, on=(User.username == IndividualRequirement.username))
                              .where((User.isStudent == 1) & (User.minorInterest == 1) & (IndividualRequirement.username.is_null(True))))

    interestedStudentList = [{'firstName': student.firstName, 'lastName': student.lastName, 'username': student.username} for student in interestedStudents]

    return interestedStudentList

def getMinorProgress():
    summerCase = Case(None, [(CertificationRequirement.name == "Summer Program", 1)], 0)

    engagedStudentsWithCount = (
        User.select(User.firstName, User.lastName, User.username, fn.COUNT(IndividualRequirement.id).alias('engagementCount'), fn.SUM(summerCase).alias('hasSummer'))
            .join(IndividualRequirement, on=(User.username == IndividualRequirement.username))
            .join(CertificationRequirement, on=(IndividualRequirement.requirement_id == CertificationRequirement.id))
            .where(CertificationRequirement.certification_id == Certification.CCE)
            .group_by(User.firstName, User.lastName, User.username)
            .order_by(fn.COUNT(IndividualRequirement.id).desc())
    )
    
    engagedStudentsList = [{'username': student.username,
                            'firstName': student.firstName,
                            'lastName': student.lastName,
                            'engagementCount': student.engagementCount - student.hasSummer,
                            'hasSummer': student.hasSummer}
        for student in engagedStudentsWithCount
    ]

    return engagedStudentsList
   
def toggleMinorInterest(username):
    """
    Given a username, update their minor interest and minor status.
    """
    user = User.get(username=username)
    user.minorInterest = not user.minorInterest

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

def setCommunityEngagementForUser(action, engagementData, currentUser):
    if engagementData['type'] not in ['program','course']:
        raise Exception("Invalid engagement type!")

    # TODO get an open requirement. What about name changing from "Summer Program"? 
    # Left join cert req and get where name is community engagement and assign to it. 

    requirement = (CertificationRequirement.select()
                                           .join(IndividualRequirement, JOIN.LEFT_OUTER, on=((IndividualRequirement.requirement_id == CertificationRequirement.id) & (IndividualRequirement.username_id == engagementData['username'])))
                                           .where(IndividualRequirement.username_id.is_null(True),
                                                  CertificationRequirement.certification_id == 2, 
                                                  CertificationRequirement.name.not_in(['Summer Program'])))
    if action == 'add':
        try: 
            IndividualRequirement.create(**{
                    engagementData['type']: engagementData['id'],
                    "username": engagementData['username'],
                    "term": engagementData['term'],
                    "requirement": requirement.get(),
                    "addedBy": currentUser,
                })
        except DoesNotExist as e:
            raise e 
        
    elif action == 'remove':
        IndividualRequirement.delete().where(
                getattr(IndividualRequirement, engagementData['type']) == engagementData['id'],
                IndividualRequirement.username == engagementData['username'],
                IndividualRequirement.term == engagementData['term']
            ).execute()
    else:
        raise Exception(f"Invalid action '{action}' sent to setCommunityEngagementForUser")


def getCommunityEngagementByTerm(username):
    """
    Given a username, return all of their community engagements (service learning courses and event participations.)
    """
    # TODO determine if engagement is already mapped to a requirement 
    courses = (Course.select(Course)
                     .join(CourseParticipant, on=(Course.id == CourseParticipant.course))
                     .where(CourseParticipant.user == username)
                     .group_by(Course.courseName, Course.term))
    
    # initialize default dict to store term descriptions as keys mapping to each
    # engagement's respective type, name, id, and term.
    terms = defaultdict(list)
    for course in courses:
        terms[(course.term.description, course.term.id)].append({
                    "name":course.courseName, 
                    "id":course.id, 
                    "type":"course", 
                    "matched": False,
                    "term":course.term.id})

    events = (Event.select(Event, Program)
                   .join(EventParticipant, on=(Event.id == EventParticipant.event)).switch()
                   .join(Program)
                   .where(EventParticipant.user == username)
                   .group_by(Event.program, Event.term))
    
    for event in events:
        terms[(event.term.description, event.term.id)].append({
                    "name":event.program.programName, 
                    "id":event.program.id, 
                    "type":"program", 
                    "matched": False,
                    "term":event.term.id
                })
    
    # sorting the terms by the term id
    return dict(sorted(terms.items(), key=lambda x: x[0][1]))

def saveOtherEngagementRequest(engagementRequest):
    otherEngagementRequest = {"user": engagementRequest['user'],
                              "experienceName": engagementRequest['experience'],
                              "term": engagementRequest['term'],
                              "description": engagementRequest['description'],
                              "company": engagementRequest['company'],
                              "weeklyHours": engagementRequest['hours'],
                              "weeks": engagementRequest['weeks'],
                              "filename": engagementRequest['attachment'],
                              "status": "Pending"}
    
    CommunityEngagementRequest.create(**otherEngagementRequest)
