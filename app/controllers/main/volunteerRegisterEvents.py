from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.controllers.main import main_bp
from app.controllers.events import events_bp
from app.logic.userRsvpForEvent import userRsvpForEvent, unattendedRequiredEvents
from flask import flash, request, redirect, url_for, g
from app import app



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
        flash(f"{userId.firstName} {userId.lastName} successfully registered. However, the following training may be required: {reqListToString}.", 'success')

    #if they are eligible
    else:
        flash("Successfully registered for event!","success")
    print(eventData['eventId'], eventData['programId'])
    print('rsvp??', (EventParticipant.select().where((EventParticipant.user == userId) &(EventParticipant.event == eventData['eventId'])& (EventParticipant.rsvp == True))).exists())
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
    flash("Successfully unregistered for event!","success")
    if 'from' in eventData:
        if eventData['from'] == 'ajax':
            return ''
    return redirect(url_for("admin.editEvent", eventId=eventId, program=program))
