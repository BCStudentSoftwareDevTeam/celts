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
    # print(userRsvpForEvent("ayisie", 3))
    EventRSVPUser = userRsvpForEvent(userId, eventId)
    print(type(EventRSVPUser))
    if EventRSVPUser == True:
        flash("Successfully registered for event!")
        return redirect(url_for('events.showUpcomingEvent'))
    else:
        print(EventRSVPUser)
        flash(f"Warning! {userId.firstName} did not do the required training")

    return EventRSVPUser
        # return (requiredEvents)
