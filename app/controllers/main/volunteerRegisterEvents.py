from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.controllers.admin import admin_bp
from app.controllers.events import events_bp
from app.logic.userRsvpForEvent import userRsvpForEvent
from flask import flash, request, redirect, url_for, g



@admin_bp.route('/rsvpForEvent', methods=['POST'])
def volunteerRegister():
    """
    This function selects the user ID and event ID and registers the user
    for the event they have clicked register for.
    """
    eventData = request.form
    userId = User.get(User.username == g.current_user)
    eventId = eventData['eventId']
    program = eventData['programId']
    isEligible, listOfRequirements = userRsvpForEvent(userId, eventId)

    if not isEligible: # if they are banned
        flash(f"Cannot RSVP: {userId.firstName} is banned")

    elif len(listOfRequirements) > 0:
        if len(listOfRequirements) >= 3:
            reqListToString = ', '.join(listOfRequirements[:-1])
            reqListToString += ' or ' + listOfRequirements[-1]
            flash(f"{userId.firstName} Registered. Warning! has not done the following required trainings: {reqListToString}")

        elif len(listOfRequirements) == 2:
            reqListToString = ' or '.join(listOfRequirements)
            flash(f"{userId.firstName} Registered. Warning! has not done the following required trainings: {reqListToString}")

        else:
            reqListToString = str(listOfRequirements[0])
            reqListToString = 'Berea Buddies'
            flash(f"{userId.firstName} Registered. Warning! has not done the following required trainings: {reqListToString}")
    #if they are eligible
    else:
        RSVPupdate =(EventParticipant.update({EventParticipant.rsvp: True})
                         .where(EventParticipant.user == userId, EventParticipant.event == eventId))
        RSVPupdate.execute()
        flash("Successfully registered for event!","success")
    return redirect(url_for("admin.editEvent", eventId=eventId, program=program))

@admin_bp.route('/rsvpRemove', methods=['POST'])
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
    flash("Successfully unregistered for event!","danger")
    return redirect(url_for("admin.editEvent", eventId=eventId, program=program))
