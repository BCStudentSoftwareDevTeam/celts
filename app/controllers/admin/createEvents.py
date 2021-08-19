from dateutil import parser
from app.models.event import Event
from flask import request
from app.controllers.admin import admin_bp
from app.logic.adminNewEvent import eventEdit
from app.logic.adminNewEvent import createNewEvent, setValueForUncheckedBox, calculateRecurringEventFrequency
from app.logic.validateNewEvent import validateNewEventData
from flask import flash, redirect, url_for, g
import json

@admin_bp.route('/makeRecurringEvents', methods=['POST'])
def addRecurringEvents():
    recurringEventInfo = request.form.copy()
    recurringEvents = calculateRecurringEventFrequency(recurringEventInfo)
    return json.dumps(recurringEvents)

@admin_bp.route('/createEvent', methods=['POST'])
def createEvent():

    if not (g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff):
        flash("Only celts admins can create an event!", 'warning')
        return redirect(url_for("main.profilePage", username = g.current_user.username))

    else:
        eventData = request.form.copy() # request.form returns a immutable dict so we need to copy to make changes
        newEventData= setValueForUncheckedBox(eventData)
        eventId = newEventData['eventId']

        #if an event is not recurring then it will have same end and start date
        if newEventData['eventEndDate'] == '':
            newEventData['eventEndDate'] = newEventData['eventStartDate']

        # function to validate data
        if eventId:
            dataIsValid, validationErrorMessage, newEventData = validateNewEventData(newEventData, checkExists=False)
        else:
            dataIsValid, validationErrorMessage, newEventData = validateNewEventData(newEventData)

        if dataIsValid:
            if not eventId:
                createNewEvent(newEventData)
                flash("Event successfully created!", 'success')
                return redirect(url_for("events.events", term = newEventData['eventTerm']))
            else:
                eventEdit(newEventData)
                flash("Event successfully updated!")
                return redirect(url_for("events.events", term = newEventData['eventTerm']))
        else:
            flash(validationErrorMessage, 'warning')
            return redirect(url_for("admin.createEventPage", program = newEventData['programId']))
