from app.models.event import Event
from app.models.user import User
from app.controllers.admin import admin_bp
from app.controllers.events import events_bp
from app.logic.userRsvpForEvent import userRsvpForEvent
from flask import flash, request, redirect, url_for, g

@admin_bp.route('/rsvpForEvent', methods=['POST'])
def volunteerRegister(eventData):
    """
    This function selects the user ID and event ID and registers the user
    for the event they have clicked register for.
    """
    userId = User.get(User.username == 'khatts')
    eventId = eventData['eventId']
    isEligible, listOfRequirements = userRsvpForEvent(userId, eventId)
    if not isEligible: # if they are banned
        flash(f"Cannot RSVP: {userId.firstName} is banned")

    elif listOfRequirements is not None:
        if not len(listOfRequirements) < 3:
            reqListToString = ', '.join(listOfRequirements[:-1])
            reqListToString += ' or ' + listOfRequirements[-1]
        elif not len(listOfRequirements) < 2:
            reqListToString = ' or '.join(listOfRequirements)
        else:
            reqListToString = str(listOfRequirements[0])
        flash(f"Warning: {userId.firstName} has not done the following required trainings: {reqListToString}")
    else:
        flash("Successfully registered for event!")
        #FIXME: This is likely where you actually update the database
    return redirect(url_for('events.showUpcomingEvent')) #FIXME: Have this redirect to the right page
