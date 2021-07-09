from dateutil import parser
from app.models.event import Event
from flask import request
from app.controllers.admin import admin_bp
from app.logic.adminNewEvent import createNewEvent, setValueForUncheckedBox, eventEdit
from app.logic.validateNewEvent import validateNewEventData
from flask import flash, redirect, url_for, g

@admin_bp.route('/createEvent', methods=['POST'])
def createEvent():

    if g.current_user.isCeltsAdmin:

        eventData = request.form.copy() #since request.form returns an immutable dict, we need to copy to change it
        newEventData= setValueForUncheckedBox(eventData)
        eventId = newEventData['eventId']

        # reformat date into y-m-d for the backend
        newEventData['eventStartDate'] = parser.parse(newEventData['eventStartDate'], dayfirst=True)
        newEventData['eventEndDate'] = parser.parse(newEventData['eventEndDate'], dayfirst=True)


        # function to validate data
        validNewEventData, eventErrorMessage = validateNewEventData(newEventData)

        if validNewEventData:
            if not eventId:

                createNewEvent(newEventData)
                flash("Event successfully created!")
                return redirect(url_for("admin.createEventPage", program=newEventData['programId']))

            else:
                eventEdit(newEventData)
                flash("Event successfully updated!")
                return redirect(url_for("admin.createEventPage", program_id=newEventData['programId']))
        else:
            flash(eventErrorMessage)
            return redirect(url_for("admin.createEventPage", program=2)) #FIXME: have this redirect to main programs page (or some appropriate non admin page).

    flash("Only CELTS admins can create an event!")
    return redirect(url_for("admin.createEventPage", program=2)) #FIXME: have this redirect to main programs page (or some appropriate non admin page).
