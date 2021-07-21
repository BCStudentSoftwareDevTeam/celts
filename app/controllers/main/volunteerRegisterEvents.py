from app.models.event import Event
from app.models.user import User
from app.controllers.admin import admin_bp
from app.controllers.events import events_bp
from app.logic.userRsvpForEvent import userRsvpForEvent
from flask import flash, redirect, url_for, g

# @admin_bp.route('/rsvpForEvent', methods=['GET'])
# def elibibilityCheck(eventData):
#     isEligibleForProgram(program,user)
#




@admin_bp.route('/rsvpForEvent', methods=['POST'])
def volunteerRegister(eventData):
    """
    This function selects the user ID and event ID and registers the user
    for the event they have clicked register for.
    """
    userId = User.get(User.username == g.current_user)
    eventId = eventData['eventId']

    if userRsvpForEvent(userId, eventId):
        flash("Successfully registered for event!")
        return redirect(url_for('events.showUpcomingEvent'))

    else:
        flash("Warning! User uneligible for event")
