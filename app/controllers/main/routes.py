from flask import request, render_template, g, abort, flash, redirect, url_for
from datetime import datetime
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
from app.controllers.main import main_bp
from app.logic.users import addUserInterest, removeUserInterest, banUser, unbanUser, isEligibleForProgram
from app.logic.participants import userRsvpForEvent, unattendedRequiredEvents, trainedParticipants
from app.logic.events import *
from app.logic.searchUsers import searchUsers
from app.logic.transcript import *
from app.logic.volunteers import setUserBackgroundCheck

@main_bp.route('/', methods=['GET'])
@main_bp.route('/events/<selectedTerm>', methods=['GET'])
def events(selectedTerm=None):
    currentTerm = g.current_term
    if selectedTerm:
        currentTerm = selectedTerm
    currentTime = datetime.datetime.now()
    term = Term.get_by_id(currentTerm)
    studentLedProgram = getStudentLedProgram(term)
    trainingProgram = getTrainingProgram(term)
    bonnerProgram = getBonnerProgram(term)
    oneTimeEvents = getOneTimeEvents(term)
    listOfTerms = Term.select()
    participantRSVP = EventRsvp.select().where(EventRsvp.user == g.current_user)
    rsvpedEventsID = [event.event.id for event in participantRSVP]


    return render_template("/events/event_list.html",
        selectedTerm = Term.get_by_id(currentTerm),
        studentLedProgram = studentLedProgram,
        trainingProgram = trainingProgram,
        bonnerProgram = bonnerProgram,
        oneTimeEvents = oneTimeEvents,
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
        return "User does not exist", 404
    if (g.current_user == username) or g.current_user.isAdmin:
         upcomingEvents = getUpcomingEventsForUser(username)
         programs = Program.select()
         interests = Interest.select().where(Interest.user == username)
         programsInterested = [interest.program for interest in interests]
         allUserEntries = list(BackgroundCheck.select().where(BackgroundCheck.user == username))
         completedBackgroundCheck = {entry.type.id: entry.passBackgroundCheck for entry in allUserEntries}
         backgroundTypes = list(BackgroundCheckType.select())
         eligibilityTable = []
         for program in programs:
              notes = ProgramBan.select().where(ProgramBan.user == username,
                                                ProgramBan.program == program,
                                                ProgramBan.endDate > datetime.datetime.now())

              noteForDict = list(notes)[-1].banNote.noteContent if list(notes) else ""
              eligibilityTable.append({"program" : program,
                                   "completedTraining" : (username in trainedParticipants(program, g.current_term)),
                                   "isNotBanned" : isEligibleForProgram(program, username),
                                   "banNote": noteForDict})
         return render_template ("/main/volunteerProfile.html",
            programsInterested = programsInterested,
            upcomingEvents = upcomingEvents,
            eligibilityTable = eligibilityTable,
            volunteer = volunteer,
            backgroundTypes = backgroundTypes,
            completedBackgroundCheck = completedBackgroundCheck
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
        flash("Successfully banned the volunteer", "success")
        return ""
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
        return addUserInterest(program_id, username)
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
        return removeUserInterest(program_id, username)

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
    return redirect(url_for("admin.editEvent", eventId=event.id))


@main_bp.route('/rsvpRemove', methods = ['POST'])
def RemoveRSVP():
    """
    This function deletes the user ID and event ID from database when RemoveRSVP  is clicked
    """
    eventData = request.form
    event = Event.get_by_id(eventData['id'])

    currentRsvpParticipant = EventRsvp.get(EventRsvp.user == g.current_user, EventRsvp.event == event)
    currentRsvpParticipant.delete_instance()

    flash("Successfully unregistered for event!", "success")
    return redirect(url_for("admin.editEvent", eventId=event.id))

@main_bp.route('/<username>/serviceTranscript', methods = ['GET'])
def serviceTranscript(username):
    user = User.get_or_none(User.username == username)
    if user is None:
        abort(404)
    if user != g.current_user and not g.current_user.isAdmin:
        abort(403)

    programs = getProgramTranscript(username)
    slCourses = getSlCourseTranscript(username)
    trainingData = getTrainingTranscript(username)
    bonnerData = getBonnerScholarEvents(username)
    totalHours = getTotalHours(username)
    startDate = getStartYear(username)

    return render_template('main/serviceTranscript.html',
                            programs = programs,
                            slCourses = slCourses.objects(),
                            trainingData = trainingData,
                            bonnerData = bonnerData,
                            totalHours = totalHours,
                            startDate = startDate,
                            userData = user)

@main_bp.route('/searchUser/<query>', methods = ['GET'])
def searchUser(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    try:
        query = query.strip()
        search = query.upper()
        splitSearch = search.split()
        searchResults = searchUsers(query)
        return searchResults
    except Exception as e:
        print(e)
        return "Error in searching for user", 500

@main_bp.route('/contributors',methods = ['GET'])
def contributors():
    return render_template("/contributors.html")



@main_bp.route('/manageservicelearning', methods = ['GET'])
def getAllCourseIntructors():
    """
    This function selects all the Intructors Name and the previous courses
    """
    users = User.select().where(User.isFaculty)
    courseInstructors = CourseInstructor.select()
    course_dict = {}

    for i in courseInstructors:
        course_dict.setdefault(i.user.firstName + " " + i.user.lastName, []).append(i.course.courseName)


    return render_template('/main/manageServiceLearningFaculty.html',courseInstructors = course_dict)
