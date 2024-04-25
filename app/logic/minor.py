from collections import defaultdict
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn, Case, DoesNotExist

from app.models.user import User
from app.models.term import Term
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

def getEngagementTotal(engagementData):
    """ 
        Count the number of engagements (from all terms) that have matched with a requirement 
    """

    # map the flattened list of engagements to their matched values, and sum them
    return sum(map(lambda e: e['matched'], sum(engagementData.values(),[])))


def getMinorInterest():
    """
        Get all students that have indicated interest in the CCE minor and return a list of dicts of all interested students
    """
    interestedStudents = (User.select(User.firstName, User.lastName, User.username)
                              .join(IndividualRequirement, JOIN.LEFT_OUTER, on=(User.username == IndividualRequirement.username))
                              .where(User.isStudent & User.minorInterest & IndividualRequirement.username.is_null(True)))

    interestedStudentList = [{'firstName': student.firstName, 'lastName': student.lastName, 'username': student.username} for student in interestedStudents]

    return interestedStudentList

def getMinorProgress():
    """
        Get all the users who have an IndividualRequirement record under the CCE certification which 
        and returns a list of dicts containing the student, how many engagements they have completed, 
        and if they have completed the summer experience. 
    """
    summerCase = Case(None, [(CertificationRequirement.name == "Summer Program", 1)], 0)

    engagedStudentsWithCount = (
        User.select(User, fn.COUNT(IndividualRequirement.id).alias('engagementCount'), 
                                                                    fn.SUM(summerCase).alias('hasSummer'),
                                                                    fn.IF(fn.COUNT(CommunityEngagementRequest.id) > 0, True, False).alias('hasCommunityEngagementRequest'))
            .join(IndividualRequirement, on=(User.username == IndividualRequirement.username))
            .join(CertificationRequirement, on=(IndividualRequirement.requirement_id == CertificationRequirement.id))
            .switch(User).join(CommunityEngagementRequest, JOIN.LEFT_OUTER, on= (User.username == CommunityEngagementRequest.user,))
            .where(CertificationRequirement.certification_id == Certification.CCE)
            .group_by(User.firstName, User.lastName, User.username)
            .order_by(fn.COUNT(IndividualRequirement.id).desc())
    )
    engagedStudentsList = [{
        'username': student.username,
        'firstName': student.firstName,
        'lastName': student.lastName,
        'engagementCount': student.engagementCount - student.hasSummer,
        'hasCommunityEngagementRequest': student.hasCommunityEngagementRequest,
        'hasSummer': "Completed" if student.hasSummer else "Incomplete",
        'hasGraduated': "Yes" if student.hasGraduated else "No" } for student in engagedStudentsWithCount]

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
    """
        Either add or remove an IndividualRequirement record for a student's Sustained Community Engagement

        :param action: The behavior of the function. Can be 'add' or 'remove'
        :param engagementData:
            type: program or course
            id: program or course id
            username: the username of the student that is having a community engagement added or removed
            term: The term the engagement is recorded in
        :param currentuser: The user who is performing the add/remove action 

        :raises DoesNotExist: if there are no available CertificationRequirement slots remaining for the engagement
    """
    if engagementData['type'] not in ['program','course']:
        raise Exception("Invalid engagement type!")

    requirement = (CertificationRequirement.select()
                       .join(IndividualRequirement, JOIN.LEFT_OUTER, on=(
                              (IndividualRequirement.requirement == CertificationRequirement.id) & 
                              (IndividualRequirement.username == engagementData['username']))) 
                       .where(IndividualRequirement.username.is_null(True),
                              CertificationRequirement.certification == Certification.CCE, 
                              CertificationRequirement.name.not_in(['Summer Program'])))
    if action == 'add':
        try: 
            IndividualRequirement.create(**{engagementData['type']: engagementData['id'],
                                           "username": engagementData['username'],
                                           "term": engagementData['term'],
                                           "requirement": requirement.get(),
                                           "addedBy": currentUser,
                                        })
        # Thrown if there are no available engagement requirements left. Handled elsewhere.
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
    courseMatchCase = Case(None, [(IndividualRequirement.course.is_null(True) , 0)], 1)

    courses = (Course.select(Course, courseMatchCase.alias("matchedReq"))
                     .join(CourseParticipant, on=(Course.id == CourseParticipant.course))
                     .join(IndividualRequirement, JOIN.LEFT_OUTER, on=(
                                (IndividualRequirement.course == Course.id) & 
                                (IndividualRequirement.username == CourseParticipant.user) & 
                                (IndividualRequirement.term == Course.term)))
                     .where(CourseParticipant.user == username)
                     .group_by(Course.courseName, Course.term))
    
    # initialize default dict to store term descriptions as keys mapping to each
    # engagement's respective type, name, id, and term.
    communityEngagementByTermDict = defaultdict(list)
    for course in courses:
        communityEngagementByTermDict[(course.term.description, course.term.id)].append(
                {"name":course.courseName,
                 "id":course.id,
                 "type":"course",
                 "matched": course.matchedReq,
                 "term":course.term.id})

    programMatchCase = Case(None, [(IndividualRequirement.program.is_null(True) , 0)], 1)

    events = (Event.select(Event, Program, programMatchCase.alias('matchedReq'))
                   .join(EventParticipant, on=(Event.id == EventParticipant.event)).switch()
                   .join(Program)
                   .join(IndividualRequirement, JOIN.LEFT_OUTER, on=((IndividualRequirement.program == Program.id) &
                                                                     (IndividualRequirement.username == EventParticipant.user) &
                                                                     (IndividualRequirement.term == Event.term)))
                   .where(EventParticipant.user == username)
                   .group_by(Event.program, Event.term))
    
    for event in events:
        communityEngagementByTermDict[(event.term.description, event.term.id)].append({"name":event.program.programName,
                                                                                       "id":event.program.id,
                                                                                       "type":"program",
                                                                                       "matched": event.matchedReq,
                                                                                       "term":event.term.id
                                                                                      })

    # sorting the communityEngagementByTermDict by the term id
    return dict(sorted(communityEngagementByTermDict.items(), key=lambda engagement: engagement[0][1]))

def saveOtherEngagementRequest(engagementRequest):
    """
        Create a CommunityEngagementRequest entry based off of the form data
    """
    engagementRequest['status'] = "Pending"
    CommunityEngagementRequest.create(**engagementRequest)
    

def saveSummerExperience(username, summerExperience, currentUser):
    """
        :param username: username of the student that the summer experience is for
        :param summerExperience: dict 
            summerExperience: string of what the summer experience was (will be written as the 'description' in the IndividualRequirement table)
            selectedSummerTerm: the term description that the summer experience took place in
        :param currentUser: the username of the user who added the summer experience record

        Delete any existing IndividualRequirement entry for 'username' if it is for 'Summer Program' and create a new IndividualRequirement entry for 
        'Summer Program' with the contents of summerExperience. 
    """
    requirementDeleteSubSelect = CertificationRequirement.select().where(CertificationRequirement.certification == Certification.CCE, CertificationRequirement.name << ['Summer Program'])
    IndividualRequirement.delete().where(IndividualRequirement.username == username, IndividualRequirement.requirement == requirementDeleteSubSelect).execute()

    requirement = (CertificationRequirement.select()
                                           .join(IndividualRequirement, JOIN.LEFT_OUTER, on=((IndividualRequirement.requirement == CertificationRequirement.id) & 
                                                                                             (IndividualRequirement.username == username)))
                                          .where(IndividualRequirement.username.is_null(True),
                                                 CertificationRequirement.certification == Certification.CCE, 
                                                 CertificationRequirement.name << ['Summer Program']))
    
    summerTerm = (Term.select().where(Term.description == summerExperience['selectedSummerTerm']))

    IndividualRequirement.create(**{"description": summerExperience['summerExperience'],
                                    "username": username,
                                    "term": summerTerm.get(),
                                    "requirement": requirement.get(),
                                    "addedBy": currentUser,
                                })
    return ""

def getSummerExperience(username):
    """
        Get a students summer experience to populate text box if the student has one
    """ 
    summerExperience = (IndividualRequirement.select()
                                             .join(CertificationRequirement, JOIN.LEFT_OUTER, on=(CertificationRequirement.id == IndividualRequirement.requirement)).switch()
                                             .join(Term, on=(IndividualRequirement.term == Term.id))
                                             .where(IndividualRequirement.username == username, 
                                                    CertificationRequirement.certification == Certification.CCE,
                                                    CertificationRequirement.name << ['Summer Program']))
    if len(list(summerExperience)) == 1:
        return (summerExperience.get().term.description, summerExperience.get().description)

    return (None, None) 

def removeSummerExperience(username): 
    """
        Delete IndividualRequirement table entry for 'username'
    """
    term, summerExperienceToDelete = getSummerExperience(username)
    IndividualRequirement.delete().where(IndividualRequirement.username == username, IndividualRequirement.description == summerExperienceToDelete).execute()


def getSummerTerms():
    """
        Return a list of all terms with the isSummer flag that is marked True. Used to populate term dropdown for summer experience
    """
    summerTerms = list(Term.select().where(Term.isSummer).order_by(Term.termOrder))

    return summerTerms
