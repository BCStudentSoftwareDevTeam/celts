from app.models.event import Event
from app.models.user import User
from app.controllers.admin import admin_bp
from app.controllers.events import userRsvpForEvent
from flask import flash, redirect, url_for, g




@admin_bp.route('/rsvpForEvent', methods=['POST'])
def volunteerRegister():
    """
    This function selects the user ID and event ID and registers the user
    for the event they have clicked register for.
    """
    userId = User.get(User == g.current_user)
    eventData = request.form.copy()
    eventId = eventData['eventId']

    if userRsvpForEvent(userId, eventId):
        flash("Successfully registered for event!")
        return "It worked"

    else:
        return "It didn't work"
