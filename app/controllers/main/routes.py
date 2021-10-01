from flask import request, render_template, g, abort, flash, redirect, url_for
from datetime import datetime

from app import app
from app.models.program import Program
from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.interest import Interest
from app.models.term import Term
from app.models.eventRsvp import EventRsvp

from app.controllers.main import main_bp
from app.logic.events import getUpcomingEventsForUser
from app.logic.users import addRemoveInterest
from app.logic.participants import userRsvpForEvent, unattendedRequiredEvents
from app.logic.events import groupEventsByCategory

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

@main_bp.route('/profile/<username>', methods = ['GET'])
def profilePage(username):
    if not g.current_user.isCeltsAdmin and not g.current_user.isCeltsStudentStaff and g.current_user.username != username:
        return "Access Denied", 403
    try:
        profileUser = User.get(User.username == username)
        upcomingEvents = getUpcomingEventsForUser(username)
        programs = Program.select()
        interests = Interest.select().where(Interest.user == profileUser)
        interests_ids = [interest.program for interest in interests]
        return render_template('/volunteer/volunteerProfile.html',
                               title="Volunteer Interest",
                               user = profileUser,
                               programs = programs,
                               interests = interests,
                               interests_ids = interests_ids,
                               upcomingEvents = upcomingEvents)
    except Exception as e:
        print(e)
        return "Error retrieving user profile", 500

@main_bp.route('/deleteInterest/<program_id>', methods = ['POST'])
@main_bp.route('/addInterest/<program_id>', methods = ['POST'])
def updateInterest(program_id):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program
    """
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

@main_bp.route('/contributors',methods = ['GET'])
def contributors():
    return render_template("/contributors.html")
