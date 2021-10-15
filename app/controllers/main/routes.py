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
from app.logic.participants import trainedParticipants
from app.logic.events import getUpcomingEventsForUser
from app.logic.events import groupEventsByCategory
from app.logic.users import isEligibleForProgram
from app.logic.users import addRemoveInterest, banUnbanUser
from app.logic.participants import userRsvpForEvent, unattendedRequiredEvents, trainedParticipants
from app.logic.searchUsers import searchUsers

@main_bp.route('/', methods=['GET'])
@main_bp.route('/events/<selectedTerm>', methods=['GET'])
def events(selectedTerm=None):
    currentTerm = g.current_term
    if selectedTerm:
        currentTerm = selectedTerm
    currentTime = datetime.now()
    eventsDict = groupEventsByCategory(currentTerm)
    listOfTerms = Term.select()
    participantRSVP = EventRsvp.select().where(EventRsvp.user == g.current_user)
    rsvpedEventsID = [event.event.id for event in participantRSVP]

    return render_template("/events/event_list.html",
        selectedTerm = Term.get_by_id(currentTerm),
        eventDict = eventsDict,
        listOfTerms = listOfTerms,
        rsvpedEventsID = rsvpedEventsID,
        currentTime = currentTime,
        user = g.current_user)

@main_bp.route('/profile/<username>', methods=['GET'])
def viewVolunteersProfile(username):
    """
    This function displays the information of a volunteer to the user
    """
    if not g.current_user.isFaculty or g.current_user.isCeltsAdmin:
         upcomingEvents = getUpcomingEventsForUser(username)
         programs = Program.select()
         interests = Interest.select().where(Interest.user == username)
         programBan = ProgramBan.select().where(ProgramBan.user == username)
         interests_ids = [interest.program for interest in interests]
         eventParticipant = EventParticipant.select().where(EventParticipant.user == username)
         currentTerm = Term.select().where(Term.isCurrentTerm == 1)
         trainingEvents = (ProgramEvent.select().join(Event).where((Event.term == currentTerm) & (Event.isTraining == 1)))
         trainingChecklist = {}
         for program in programs:
             trainingChecklist[program.id] = trainedParticipants(program.id)
         print("-------------------------------------------------------")
         eligibilityTable = []
         for i in programs:
             eligibilityTable.append({"program" : i,
                                      "completedTraining" : (username in trainedParticipants(i)),
                                      "isNotBanned" : isEligibleForProgram(i, username)})
         return render_template ("/main/volunteerProfile.html",
            programs = programs,
            eventParticipant = eventParticipant,
            interests = interests,
            trainingEvents = trainingEvents,
            programBan = programBan,
            interests_ids = interests_ids,
            trainingChecklist = trainingChecklist,
            upcomingEvents = upcomingEvents,
            eligibilityTable = eligibilityTable,
            volunteer = User.get(User.username == username),
            user = g.current_user)
    abort(403)


@main_bp.route('/banUnbanUser/<program_id>/<username>', methods=['POST'])
def banUser(program_id, username):
    """
    This function updates the ban status of a username either when they are banned or unbanned from a program.
    """
    print("inside pythong")
    postData = request.form
    print(postData)
    banNote = postData["note"]
    banOrUnban = postData["banOrUnban"]
    username = postData["username"]
    banEndDate = postData["endDate"]
    programID = postData["programID"]

    rule = request.url_rule
    username = username
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
    print("inside delete/add interest")
    rule = request.url_rule
    username = username
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
