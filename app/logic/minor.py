from collections import defaultdict
from typing import List, Dict
from flask import flash, g
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn, Case, DoesNotExist, SQL
import xlsxwriter

from app.models import app
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
from app.models.cceMinorProposal import CCEMinorProposal
from app.logic.fileHandler import FileHandler
from app.logic.utils import getFilesFromRequest
from app.models.attachmentUpload import AttachmentUpload


def createSummerExperience(username, formData):
    """
        Given the username of the student and the formData which includes all of
        the SummerExperience information, create a new SummerExperience object.
    """
    user = User.get(User.username == username)
    contentAreas = ', '.join(formData.getlist('contentArea')) # Combine multiple content areas
    formData = dict(formData)
    formData.pop("contentArea")
    return CCEMinorProposal.create(
        student=user,
        proposalType = 'Summer Experience',
        contentAreas = contentAreas,
        createdBy = g.current_user,
        **formData,
    )

def updateSummerExperience(proposalID, formData):
    """
        Given the username of the student and the formData which includes all of
        the SummerExperience information, create a new SummerExperience object.
    """
    contentAreas = ', '.join(formData.getlist('contentArea')) # Combine multiple content areas
    formData = dict(formData)
    formData.pop("contentArea")
    formData.pop("experienceHoursOver300")
    CCEMinorProposal.update(contentAreas=contentAreas, **formData).where(CCEMinorProposal.id == proposalID).execute()

def getCCEMinorProposals(username):
    return list(CCEMinorProposal.select().where(CCEMinorProposal.student==username))

def getEngagementTotal(engagementData):
    """ 
        Count the number of engagements (from all terms) that have matched with a requirement 
    """

    # map the flattened list of engagements to their matched values, and sum them
    return sum(map(lambda e: e['matched'], sum(engagementData.values(),[])))


def getMinorInterest() -> List[Dict]:
    """
        Get all students that have indicated interest in the CCE minor and return a list of dicts of all interested students
    """
    interestedStudents = (User.select(User)
                              .join(IndividualRequirement, JOIN.LEFT_OUTER, on=(User.username == IndividualRequirement.username))
                              .where(User.isStudent & User.minorInterest & ~User.declaredMinor & IndividualRequirement.username.is_null(True)))

    interestedStudentList = [model_to_dict(student) for student in interestedStudents]

    return interestedStudentList

def getMinorProgress():
    """
        Get all the users who have an IndividualRequirement record under the CCE certification which 
        and returns a list of dicts containing the student, how many engagements they have completed, 
        and if they have completed the summer experience. 
    """
    summerCase = Case(None, [(CCEMinorProposal.proposalType == "Summer Experience", 1)], 0)

    engagedStudentsWithCount = (
        User.select(User, fn.COUNT(IndividualRequirement.id).alias('engagementCount'), 
                                                                    fn.SUM(summerCase).alias('hasSummer'),
                                                                    fn.IF(fn.COUNT(CCEMinorProposal.id) > 0, True, False).alias('hasCCEMinorProposal'))
            .join(IndividualRequirement, on=(User.username == IndividualRequirement.username))
            .join(CertificationRequirement, on=(IndividualRequirement.requirement_id == CertificationRequirement.id))
            .switch(User).join(CCEMinorProposal, JOIN.LEFT_OUTER, on= (User.username == CCEMinorProposal.student))
            .where(
                (CertificationRequirement.certification_id == Certification.CCE) &
                (User.declaredMinor == True)
            )
            .group_by(User.firstName, User.lastName, User.username)
            .order_by(SQL("engagementCount").desc())
    )
    engagedStudentsList = [{'firstName': student.firstName,
                            'lastName': student.lastName,
                            'username': student.username,
                            'B-Number': student.bnumber,
                            'hasGraduated': student.hasGraduated, 
                            'engagementCount': student.engagementCount - student.hasSummer,
                            'hasCCEMinorProposal': student.hasCCEMinorProposal,
                            'hasSummer': "Completed" if student.hasSummer else "Incomplete"} for student in engagedStudentsWithCount]
    return engagedStudentsList

def getMinorSpreadsheet():
    """
        Returns a spreadsheet containing users and related spreadsheet information.
    """
    # If we're in 2025, can we get the minor information for 2023?
    studentProgress = getMinorProgress()
    columnNames = studentProgress[0]
    columnNames = ["First Name", "Last Name", "Username", "B-Number", "Number of Engagements", "Completed Summer Experience"]

    filepath = f"{app.config['files']['base_path']}/minor_data.xlsx"
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})

    worksheet = workbook.add_worksheet('minor_information')
    format_row = workbook.add_format({'align': 'left'})

    columnIndex = 1
    worksheet.set_column(columnIndex, len(columnNames), 30, workbook.add_format({'bold': True}))
    for columnName in columnNames:
        worksheet.write(1, columnIndex, columnName)
        columnIndex += 1

    for rowNumber, student in enumerate(studentProgress, 2):
        if student['hasGraduated']: continue
        student.pop('hasCCEMinorProposal')
        student.pop('hasGraduated')
        student['hasSummer'] = "Yes" if student['hasSummer'] == "Complete" else "No"
        worksheet.set_row(rowNumber, None, format_row)
        if student['B-Number'] == None: student["B-Number"] = "No B-Number Found"
        for columnNumber, key in enumerate(student, 1):
            worksheet.write(rowNumber, columnNumber, student[key])

    
    workbook.close()
    
    return filepath


def toggleMinorInterest(username, isAdding):
    """
        Given a username, update their minor interest and minor status.
    """
    
    try:
        user = User.get(username=username)
        if not user:
            return {"error": "User not found"}, 404
        
        user.minorInterest = isAdding
        user.declaredMinor = False
        user.save()

    except Exception as e:
        print(f"Error updating minor interest: {e}")
        return {"error": str(e)}, 500
    
def declareMinorInterest(username):
    """
    Given a username, update their minor declaration
    """
    user = User.get_by_id(username)
    
    if not user:
        raise ValueError(f"User with username '{username}' not found.")
    
    user.declaredMinor = not user.declaredMinor
    
    try:
        user.save()
    except Exception as e:
        raise RuntimeError(f"Failed to declare interested student: {e}")
    
def getDeclaredMinorStudents():
    """
    This function retrieves a list of students who have declared the CCE minor along with their engagement progress.
    It returns a list of dictionaries containing student information and their engagement details and adds students who have no requirements but have declared the minor with 0 engagements.
    """
    summerEngagementCount = fn.COUNT(
        fn.DISTINCT(
            Case(
                None,
                [(CCEMinorProposal.proposalType == "Summer Experience", CCEMinorProposal.id)],
                None
            )
        )
    ).alias("summerEngagementCount")

    # this returns the count of distinct engagements that have a certification requirement id.
    # this is important because our join clause specifically joins individualrequirements with the certifications that match to CCE
    # while leaving the rest as null
    cceEngagementCount = fn.COUNT(
        fn.DISTINCT(
            Case(
                None,
                [(CertificationRequirement.id.is_null(False), IndividualRequirement.id)],
                None
            )
        )
    ).alias("allEngagementCount")

    q = (
        User
        .select(
            User,
            cceEngagementCount,
            summerEngagementCount,
            fn.IF(fn.COUNT(fn.DISTINCT(CCEMinorProposal.id)) > 0, True, False).alias("hasCCEMinorProposal"),
        )
        .join(IndividualRequirement, JOIN.LEFT_OUTER, on=(User.username == IndividualRequirement.username))
        .join(CertificationRequirement, JOIN.LEFT_OUTER, on=(
            (IndividualRequirement.requirement_id == CertificationRequirement.id) &
            (CertificationRequirement.certification_id == Certification.CCE)    # only cce minor certs are populated with non-null
            ))
        .switch(User)
        .join(CCEMinorProposal, JOIN.LEFT_OUTER, on=(User.username == CCEMinorProposal.student))
        .where(
            (User.declaredMinor == True) & 
            (User.isStudent == True)
            )
        .group_by(User.username)
        .order_by(SQL("allEngagementCount").desc())
    )

    result = []
    for s in q:
        engagementCount = int(s.allEngagementCount or 0)
        result.append({
            "firstName": s.firstName,
            "lastName": s.lastName,
            "username": s.username,
            "B-Number": s.bnumber,
            "email": s.email,
            "hasGraduated": s.hasGraduated,
            "engagementCount": engagementCount,
            "hasCCEMinorProposal": bool(s.hasCCEMinorProposal),
            "hasSummer": "Completed" if (s.summerEngagementCount and int(s.summerEngagementCount) > 0) else "Incomplete",
        })

    return result
    
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
    eventsInProgramAndTerm = (Event.select(Event.id, Event.name, EventParticipant.hoursEarned)
                                   .join(Program).switch()
                                   .join(EventParticipant)
                                   .where(EventParticipant.user == username,
                                          Event.term == term_id,
                                          Event.isService == True,
                                          Program.id == program_id)
                             )
    
    program = Program.get_by_id(program_id)

    # calculate total amount of hours for the whole program that term
    totalHours = 0
    for event in eventsInProgramAndTerm:
        if event.eventparticipant.hoursEarned:
            totalHours += event.eventparticipant.hoursEarned
    
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
                   .where(EventParticipant.user == username, Event.isService == True)
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

def createOtherEngagement(username, request):
    """
    Create a CCEMinorProposal entry based off of the form data
    """
    user = User.get(User.username == username)

    createdProposal = CCEMinorProposal.create(proposalType = 'Other Engagement',
                                              createdBy = g.current_user,
                                              student = user,
                                              **request.form
                            )
    proposalObject = CCEMinorProposal.get_by_id(createdProposal)
    attachment = request.files.get("attachmentObject")
    if attachment:
        addFile = FileHandler(getFilesFromRequest(request), proposalId=createdProposal.id)
        addFile.saveFiles(parentEvent=proposalObject)

def updateOtherEngagementRequest(proposalID, request):
    """
    Update an existing CCEMinorProposal entry based off of the form data
    """
    newAttachment = request.files.get("attachmentObject")
    previousAttachment = AttachmentUpload.get_or_none(proposal=proposalID)
    proposalObject = CCEMinorProposal.get_by_id(proposalID)

    if newAttachment:
        if previousAttachment:
            FileHandler(proposalId=proposalID).deleteFile(previousAttachment.id)
        addFile = FileHandler(getFilesFromRequest(request), proposalId=proposalID)
        addFile.saveFiles(parentEvent=proposalObject)

    CCEMinorProposal.update(**request.form).where(CCEMinorProposal.id == proposalID).execute()
                
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

def removeProposal(proposalID) -> None:
    """
    Delete summer experience or other engagement objects from the CCEMinorProposal table. 
    File objects attached to the CCEMinorProposal object are also deleted. 
    """
    proposalID = int(proposalID)

    proposalAttachment = AttachmentUpload.get_or_none(proposal=proposalID)
    if proposalAttachment:
        proposalFileHandler = FileHandler(proposalId=proposalID)
        proposalFileHandler.deleteFile(proposalAttachment.id)

    CCEMinorProposal.delete().where(CCEMinorProposal.id == proposalID).execute()

def changeProposalStatus(proposalID, newStatus) -> None:
    """
    Changes the status of a proposal.
    """
    CCEMinorProposal.update(status=newStatus).where(CCEMinorProposal.id == int(proposalID)).execute()
