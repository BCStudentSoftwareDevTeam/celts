from app.models.event import Event
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.controllers.admin import admin_bp
from app.controllers.events import events_bp
from app.logic.userRsvpForEvent import userRsvpForEvent
from flask import flash, request, redirect, url_for, g
# from flask import Fl

@admin_bp.route('/rsvpForEvent', methods=['POST'])
def volunteerRegister():
    """
    This function selects the user ID and event ID and registers the user
    for the event they have clicked register for.
    """
    eventData = request.form
    userId = User.get(User.username == g.current_user)
    eventId = eventData['eventId']
    isEligible, listOfRequirements = userRsvpForEvent(userId, eventId)
    print(listOfRequirements)
    if not isEligible: # if they are banned
        flash(f"Cannot RSVP: {userId.firstName} is banned")

    elif len(listOfRequirements) > 0:
        print(listOfRequirements)
        if len(listOfRequirements) >= 3:
            reqListToString = ', '.join(listOfRequirements[:-1])
            reqListToString += ' or ' + listOfRequirements[-1]
            flash(f"Warning: {userId.firstName} has not done the following required trainings: {reqListToString}")

        elif len(listOfRequirements) == 2:
            reqListToString = ' or '.join(listOfRequirements)
            flash(f"Warning: {userId.firstName} has not done the following required trainings: {reqListToString}")

        else:
            reqListToString = str(listOfRequirements[0])
            reqListToString = 'Berea Buddies'
            flash(f"Warning: {userId.firstName} has not done the following required trainings: {reqListToString}")

    else:
        # flash("Successfully registered for event!")
        print("nice")
        RSVPupdate =(EventParticipant.update({EventParticipant.rsvp: True})
                         .where(EventParticipant.user == userId, EventParticipant.event == eventId))
        print(RSVPupdate)
        RSVPupdate.execute()
        flash("Successfully registered for event!","success")
        print('nice')
    # return ''
    return redirect(url_for("admin.addParticipants")) #FIXME: Have this redirect to the right page
