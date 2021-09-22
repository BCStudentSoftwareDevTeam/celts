from flask import request, render_template, g, abort, flash, redirect, url_for
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.program import Program
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.interest import Interest
from app.models.event import Event
from app.models.programBan import ProgramBan
from app.models.programEvent import ProgramEvent
from app.models.term import Term
from app.logic.participants import trainedParticipants
from app.logic.events import getUpcomingEventsForUser
from app.logic.users import isEligibleForProgram
from app.logic.users import addRemoveInterest
from app.logic.participants import userRsvpForEvent, unattendedRequiredEvents
from app.controllers.main import main_bp


@main_bp.route('/')
def home():
    print(f"{g.current_user.username}: {g.current_user.firstName} {g.current_user.lastName}")
    return render_template('main/home.html', title="Welcome to CELTS!")

@main_bp.route('/profile/<username>', methods=['GET'])
def viewVolunteersProfile(username):
    """
    This function displays the information of a volunteer to the user
    """
    print(g.current_user)
    if not g.current_user.isFaculty or g.current_user.isCeltsAdmin:
         upcomingEvents = getUpcomingEventsForUser(username)
         programs = Program.select()
         interests = Interest.select().where(Interest.user == username)
         programBan = ProgramBan.select().where(ProgramBan.user == username)
         interests_ids = [interest.program for interest in interests]
         eventParticipant = EventParticipant.select().where(EventParticipant.user == username)
         trainingEvents = Event.select()
          # trainingEvents = ProgramEvent.select().where(ProgramEvent.event.term.isBreak == 1)
         for event in trainingEvents:
             print(event.eventName)
         # volunteertTraining = trainedParticipants()
         print("-------------------------------------------------------")
         eligibilityTable = []
         for i in programs:
             # print(i.programName, " ", (username in trainedParticipants(i)), " ", isEligibleForProgram(i, username))
             eligibilityTable.append({"program" : i,
                                      "completedTraining" : (username in trainedParticipants(i)),
                                      "isNotBanned" : isEligibleForProgram(i, username)})
         print(eligibilityTable)
         return render_template ("/main/volunteerProfile.html",
            programs = programs,
            eventParticipant = eventParticipant,
            interests = interests,
            trainingEvents = trainingEvents,
            programBan = programBan,
            interests_ids = interests_ids,
            upcomingEvents = upcomingEvents,
            eligibilityTable = eligibilityTable,
            volunteer = User.get(User.username == username),
            user = g.current_user)
    abort(403)


@main_bp.route('/deleteInterest/<program_id>', methods = ['POST'])
@main_bp.route('/addInterest/<program_id>', methods = ['POST'])
def updateInterest(program_id):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program
    """
    print("inside delete/add interest")
    rule = request.url_rule
    user = g.current_user
    try:
        return addRemoveInterest(rule, program_id, user)

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
    userId = g.current_user
    isEligible = userRsvpForEvent(userId, eventData['eventId'])
    listOfRequirements = unattendedRequiredEvents(eventData['programId'], userId)

    if not isEligible: # if they are banned
        flash(f"Cannot RSVP. Contact CELTS administrators: {app.config['celts_admin_contact']}.", "danger")

    elif listOfRequirements:
        reqListToString = ', '.join(listOfRequirements)
        flash(f"{userId.firstName} {userId.lastName} successfully registered. However, the following training may be required: {reqListToString}.", "success")

    #if they are eligible
    else:
        flash("Successfully registered for event!","success")
    if 'from' in eventData:
        if eventData['from'] == 'ajax':
            return ''
    return redirect(url_for("admin.editEvent", eventId=eventData['eventId'], program=eventData['programId']))


@main_bp.route('/rsvpRemove', methods = ['POST'])
def RemoveRSVP():
    """
    This function deletes the user ID and event ID from database when RemoveRSVP  is clicked
    """
    eventData = request.form
    userId = User.get(User.username == g.current_user)
    eventId = eventData['eventId']
    program = eventData['programId']
    currentEventParticipant = EventParticipant.get(EventParticipant.user == userId, EventParticipant.event == eventId)
    currentEventParticipant.delete_instance()

    flash("Successfully unregistered for event!", "success")
    return redirect(url_for("admin.editEvent", eventId=eventId, program=program))
