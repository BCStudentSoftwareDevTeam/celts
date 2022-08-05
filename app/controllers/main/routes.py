from flask import request, render_template, g, abort, flash, redirect, url_for, session
import datetime
import json
from http import cookies

from app import app
from app.models.program import Program
from app.models.event import Event
from app.models.backgroundCheck import BackgroundCheck
from app.models.backgroundCheckType import BackgroundCheckType
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.interest import Interest
from app.models.event import Event
from app.models.programBan import ProgramBan
from app.models.programEvent import ProgramEvent
from app.models.term import Term
from app.models.eventRsvp import EventRsvp
from app.models.note import Note
from app.models.programManager import ProgramManager
from app.models.courseStatus import CourseStatus
from app.controllers.main import main_bp
from app.logic.loginManager import logout
from app.logic.users import addUserInterest, removeUserInterest, banUser, unbanUser, isEligibleForProgram
from app.logic.participants import userRsvpForEvent, unattendedRequiredEvents, trainedParticipants, getUserParticipatedEvents, checkUserAddedToEvent
from app.logic.events import *
from app.logic.searchUsers import searchUsers
from app.logic.transcript import *
from app.logic.manageSLFaculty import getCourseDict
from app.logic.courseManagement import unapprovedCourses, approvedCourses
from app.logic.utils import selectSurroundingTerms
from app.models.courseInstructor import CourseInstructor

@main_bp.route('/logout', methods=['GET'])
def redirectToLogout():
    return redirect(logout())

@main_bp.route('/', methods=['GET'])
def redirectToEventsList():
    return redirect(url_for("main.events", selectedTerm=g.current_term))

@main_bp.route('/eventsList/<selectedTerm>', methods=['GET'])
def events(selectedTerm):
    currentTerm = g.current_term
    if selectedTerm:
        currentTerm = selectedTerm
    currentTime = datetime.datetime.now()
    listOfTerms = Term.select()
    participantRSVP = EventRsvp.select().where(EventRsvp.user == g.current_user)
    rsvpedEventsID = [event.event.id for event in participantRSVP]
    term = Term.get_by_id(currentTerm)
    studentLedEvents = getStudentLedEvents(term)
    trainingEvents = getTrainingEvents(term)
    bonnerEvents = getBonnerEvents(term)
    otherEvents = getOtherEvents(term)

    return render_template("/events/event_list.html",
        selectedTerm = term,
        studentLedEvents = studentLedEvents,
        trainingEvents = trainingEvents,
        bonnerEvents = bonnerEvents,
        otherEvents = otherEvents,
        listOfTerms = listOfTerms,
        rsvpedEventsID = rsvpedEventsID,
        currentTime = currentTime,
        user = g.current_user)

@main_bp.route('/profile/<username>', methods=['GET'])
def viewVolunteersProfile(username):
    """
    This function displays the information of a volunteer to the user
    """
    try:
        volunteer = User.get(User.username == username)
    except Exception as e:
        if g.current_user.isAdmin:
            flash(f"{username} does not exist! ", category='danger')
            return redirect(url_for('admin.studentSearchPage'))
        else:
            abort(403)  # Error 403 if non admin/student-staff user trys to access via url

    if (g.current_user == volunteer) or g.current_user.isAdmin:
        upcomingEvents = getUpcomingEventsForUser(volunteer)
        programs = Program.select()
        if not g.current_user.isBonnerScholar and not g.current_user.isAdmin:
            programs = programs.where(Program.isBonnerScholars == False)
        interests = Interest.select().where(Interest.user == volunteer)
        programsInterested = [interest.program for interest in interests]

        rsvpedEventsList = EventRsvp.select().where(EventRsvp.user == volunteer)
        rsvpedEvents = [event.event.id for event in rsvpedEventsList]

        programManagerPrograms = ProgramManager.select().where(ProgramManager.user == volunteer)
        permissionPrograms = [entry.program.id for entry in programManagerPrograms]

        allUserEntries = BackgroundCheck.select().where(BackgroundCheck.user == volunteer)

        if g.current_user.isCeltsAdmin:
            completedBackgroundCheck = {entry.type: [entry.passBackgroundCheck, entry.dateCompleted] for entry in allUserEntries}
        else:
            # sets the values to strings because student staff do not have access to input boxes
            completedBackgroundCheck = {entry.type: ['Yes' if entry.passBackgroundCheck else 'No',
                                                    '' if entry.dateCompleted == None
                                                    else entry.dateCompleted.strftime('%m/%d/%Y')] for entry in allUserEntries}

        backgroundTypes = list(BackgroundCheckType.select())
        # creates data structure for background checks that are not currently completed
        for checkType in backgroundTypes:
            if checkType not in completedBackgroundCheck.keys():
                completedBackgroundCheck[checkType] = ["No"]

        eligibilityTable = []
        for program in programs:
            notes = ProgramBan.select().where(ProgramBan.user == volunteer,
                                              ProgramBan.program == program,
                                              ProgramBan.endDate > datetime.datetime.now())

            userParticipatedEvents = getUserParticipatedEvents(program, g.current_user, g.current_term)
            noteForDict = notes[-1].banNote.noteContent if notes else ""
            eligibilityTable.append({"program": program,
                                   "completedTraining": (volunteer.username in trainedParticipants(program, g.current_term)),
                                   "trainingList": userParticipatedEvents,
                                   "isNotBanned": True if not notes else False,
                                   "banNote": noteForDict})
        return render_template ("/main/volunteerProfile.html",
                programs = programs,
                programsInterested = programsInterested,
                upcomingEvents = upcomingEvents,
                rsvpedEvents = rsvpedEvents,
                permissionPrograms = permissionPrograms,
                eligibilityTable = eligibilityTable,
                volunteer = volunteer,
                backgroundTypes = backgroundTypes,
                completedBackgroundCheck = completedBackgroundCheck,
                currentDateTime = datetime.datetime.now()
            )
    abort(403)

# ===========================Ban===============================================
@main_bp.route('/<username>/ban/<program_id>', methods=['POST'])
def ban(program_id, username):
    """
    This function updates the ban status of a username either when they are banned from a program.
    program_id: the primary id of the program the student is being banned from
    username: unique value of a user to correctly identify them
    """
    postData = request.form
    banNote = postData["note"] # This contains the note left about the change
    banEndDate = postData["endDate"] # Contains the date the ban will no longer be effective
    try:
        banUser(program_id, username, banNote, banEndDate, g.current_user)
        programInfo = Program.get(int(program_id))
        flash("Successfully banned the volunteer", "success")
        createLog(f'Banned {username} from {programInfo.programName} until {banEndDate}.')
        return "Successfully banned the volunteer."
    except Exception as e:
        print("Error  while updating ban", e)
        flash("Failed to ban the volunteer", "danger")
        return "Failed to ban the volunteer", 500

# ===========================Unban===============================================
@main_bp.route('/<username>/unban/<program_id>', methods=['POST'])
def unban(program_id, username):
    """
    This function updates the ban status of a username either when they are unbanned from a program.
    program_id: the primary id of the program the student is being unbanned from
    username: unique value of a user to correctly identify them
    """
    postData = request.form
    unbanNote = postData["note"] # This contains the note left about the change
    try:
        unbanUser(program_id, username, unbanNote, g.current_user)
        programInfo = Program.get(int(program_id))
        createLog(f'Unbanned {username} from {programInfo.programName}.')
        flash("Successfully unbanned the volunteer", "success")
        return "Successfully unbanned the volunteer"

    except Exception as e:
        print("Error  while updating Unban", e)
        flash("Failed to unban the volunteer", "danger")
        return "Failed to unban the volunteer", 500


@main_bp.route('/<username>/addInterest/<program_id>', methods=['POST'])
def addInterest(program_id, username):
    """
    This function adds a program to the list of programs a user interested in
    program_id: the primary id of the program the student is adding interest of
    username: unique value of a user to correctly identify them
    """
    try:
        success = addUserInterest(program_id, username)
        if success:
            flash("Successfully added " + Program.get_by_id(program_id).programName + " as an interest", "success")
            return ""
        else:
            flash("Was unable to remove " + Program.get_by_id(program_id).programName + " as an interest.", "danger")

    except Exception as e:
        print(e)
        return "Error Updating Interest", 500

@main_bp.route('/<username>/removeInterest/<program_id>', methods=['POST'])
def removeInterest(program_id, username):
    """
    This function removes a program to the list of programs a user interested in
    program_id: the primary id of the program the student is adding interest of
    username: unique value of a user to correctly identify them
    """
    try:
        removed = removeUserInterest(program_id, username)
        if removed:
            flash("Successfully removed " + Program.get_by_id(program_id).programName + " as an interest.", "success")
            return ""
        else:
            flash("Was unable to remove " + Program.get_by_id(program_id).programName + " as an interest.", "danger")
    except Exception as e:
        print(e)
        return "Error Updating Interest", 500

@main_bp.route('/rsvpForEvent', methods = ['POST'])
def volunteerRegister():
    """
    This function selects the user ID and event ID and registers the user
    for the event they have clicked register for.
    """
    eventData = request.form
    event = Event.get_by_id(eventData['id'])

    user = g.current_user
    isAdded = checkUserAddedToEvent(user, event)
    if not isAdded:
        isEligible = userRsvpForEvent(user, event.id)
        listOfRequirements = unattendedRequiredEvents(event.singleProgram, user)

        if not isEligible: # if they are banned
            flash(f"Cannot RSVP. Contact CELTS administrators: {app.config['celts_admin_contact']}.", "danger")

        elif listOfRequirements:
            reqListToString = ', '.join(listOfRequirements)
            flash(f"{user.firstName} {user.lastName} successfully registered. However, the following training may be required: {reqListToString}.", "success")

        #if they are eligible
        else:
            flash("Successfully registered for event!","success")

    if 'from' in eventData:
        if eventData['from'] == 'ajax':
            return ''
    return redirect(url_for("admin.eventDisplay", eventId=event.id))

@main_bp.route('/rsvpRemove', methods = ['POST'])
def RemoveRSVP():
    """
    This function deletes the user ID and event ID from database when RemoveRSVP is clicked
    """
    eventData = request.form
    event = Event.get_by_id(eventData['id'])

    currentRsvpParticipant = EventRsvp.get(EventRsvp.user == g.current_user, EventRsvp.event == event)
    currentRsvpParticipant.delete_instance()
    flash("Successfully unregistered for event!", "success")
    if 'from' in eventData:
        if eventData['from'] == 'ajax':
            return ''
    return redirect(url_for("admin.eventDisplay", eventId=event.id))

@main_bp.route('/profile/<username>/serviceTranscript', methods = ['GET'])
def serviceTranscript(username):
    user = User.get_or_none(User.username == username)
    if user is None:
        abort(404)
    if user != g.current_user and not g.current_user.isAdmin:
        abort(403)

    slCourses = getSlCourseTranscript(username)
    totalHours = getTotalHours(username)
    allEventTranscript = getAllEventTranscript(username)
    startDate = getStartYear(username)

    return render_template('main/serviceTranscript.html',
                            allEventTranscript = allEventTranscript,
                            slCourses = slCourses.objects(),
                            totalHours = totalHours,
                            startDate = startDate,
                            userData = user)

@main_bp.route('/searchUser/<query>', methods = ['GET'])
def searchUser(query):

    category= request.args.get("category")

    '''Accepts user input and queries the database returning results that matches user search'''
    try:
        query = query.strip()
        search = query.upper()
        splitSearch = search.split()
        searchResults = searchUsers(query,category)
        return searchResults
    except Exception as e:
        print(e)
        return "Error in searching for user", 500

@main_bp.route('/contributors',methods = ['GET'])
def contributors():
    return render_template("/contributors.html")

@main_bp.route('/proposalReview/', methods = ['GET', 'POST'])
def reviewProposal():
    """
    this function gets the submitted course id and returns the its data to the review proposal modal
    """
    courseID=request.form
    course=Course.get_by_id(courseID["course_id"])
    instructors_data=course.courseInstructors
    return render_template('/main/reviewproposal.html',
                            course=course,
                            instructors_data=instructors_data)

@main_bp.route('/manageServiceLearning', methods = ['GET', 'POST'])
@main_bp.route('/manageServiceLearning/<term>', methods = ['GET', 'POST'])
def getAllCourseInstructors(term=None):
    """
    This function selects all the Instructors Name and the previous courses
    """
    if g.current_user.isCeltsAdmin:
        setRedirectTarget("/manageServiceLearning")
        courseDict = getCourseDict()

        term = Term.get_or_none(Term.id == term) or g.current_term

        unapproved = unapprovedCourses(term)
        approved = approvedCourses(term)
        terms = selectSurroundingTerms(g.current_term)

        return render_template('/main/manageServiceLearningFaculty.html',
                                courseInstructors = courseDict,
                                unapprovedCourses = unapproved,
                                approvedCourses = approved,
                                terms = terms,
                                term = term,
                                CourseStatus = CourseStatus)
    else:
        abort(403)

def getRedirectTarget(popTarget=False):
    """
    This function returns a string with the URL or route to a page in the Application
        saved with setRedirectTarget() and is able to pop the value from the session
        to make it an empty value
    popTarget: expects a bool value to determine whether or not to reset
                redirectTarget to an emtpy value
    return: a string with the URL or route to a page in the application that was
            saved in setRedirectTarget()
    """
    if "redirectTarget" not in session:
        return ''

    target = session["redirectTarget"]
    if popTarget:
        session.pop("redirectTarget")
    return target

def setRedirectTarget(target):
    """
    This function saves the target URL in the session for future redirection
        to said page
    target: expects a string that is a URL or a route to a page in the application
    return: None
    """
    session["redirectTarget"] = target
