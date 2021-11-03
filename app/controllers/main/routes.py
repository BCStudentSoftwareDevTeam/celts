from flask import request, render_template, g, abort, flash, redirect, url_for
from datetime import datetime
from app import app
from app.models.program import Program
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.interest import Interest
from app.models.event import Event
from app.models.programBan import ProgramBan
from app.models.programEvent import ProgramEvent
from app.models.term import Term
from app.models.eventRsvp import EventRsvp
from app.controllers.main import main_bp
from app.logic.users import addRemoveInterest, banUnbanUser, isEligibleForProgram
from app.logic.participants import userRsvpForEvent, unattendedRequiredEvents, trainedParticipants
from app.logic.events import *
from app.logic.searchUsers import searchUsers
from app.logic.transcript import *

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
        # User.get(User.username == username)
        volunteer = User.get(User.username == username)
    except Exception as e:
        print(e)
        return "User does not exist", 404
    if (g.current_user.username == username) or g.current_user.isAdmin:
         upcomingEvents = getUpcomingEventsForUser(volunteer)
         programs = Program.select()
         interests = Interest.select().where(Interest.user == volunteer)
         programsInterested = [interest.program for interest in interests]
         # trainingChecklist = {}
         # for program in programs:
         #     trainingChecklist[program.id] = trainedParticipants(program.id)
         eligibilityTable = []
         for program in programs:
              notes = ProgramBan.select().where(ProgramBan.user == volunteer,
                                                ProgramBan.program == program,
                                                ProgramBan.endDate > datetime.datetime.now())
              noteForDict = "None"
              for j in notes:
                  noteForDict = j.banNote.noteContent
              eligibilityTable.append({"program" : program,
                                       "completedTraining" : (volunteer in trainedParticipants(program)),
                                       "isNotBanned" : isEligibleForProgram(program, volunteer),
                                       "banNote": noteForDict})
         return render_template ("/main/volunteerProfile.html",
            programs = programs,
            interests = interests,
            programsInterested = programsInterested,
            # trainingChecklist = trainingChecklist,
            upcomingEvents = upcomingEvents,
            eligibilityTable = eligibilityTable,
            volunteer = volunteer,
            user = g.current_user)
    abort(403)


@main_bp.route('/banUnbanUser/<program_id>/<username>', methods=['POST'])
def banUser(program_id, username):
    """
    This function updates the ban status of a username either when they are banned or unbanned from a program.
    program_id: the primary id of the program the student is being banned or unbanned from
    username: unique value of a user to correctly identify them
    """
    postData = request.form
    banNote = postData["note"] # This contains the note left about the change
    banOrUnban = postData["banOrUnban"] # Contains "Ban" or "Unban" to determine whether to ban or unban the user
    banEndDate = postData["endDate"] # Contains the date the ban will no longer be effective
    try:
        return banUnbanUser(banOrUnban, program_id, username, banNote, banEndDate, g.current_user)
    except Exception as e:
        print(e)
        return "Error Updating Ban", 500


@main_bp.route('/deleteInterest/<program_id>/<username>', methods = ['POST'])
@main_bp.route('/addInterest/<program_id>/<username>', methods = ['POST'])
def updateInterest(program_id, username):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program
    """
    rule = request.url_rule
    try:
        return addRemoveInterest(rule, program_id, username)

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
