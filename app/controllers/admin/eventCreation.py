from dateutil import parser
from app.models.event import Event
from flask import request, render_template
from app.models.program import Program
from app.models.term import Term
from app.controllers.admin import admin_bp
from app.logic.events import eventEdit, getAllFacilitators
from app.logic.eventCreation import createNewEvent, setValueForUncheckedBox, calculateRecurringEventFrequency
from app.logic.eventCreation import validateNewEventData
from app.logic.utils import selectFutureTerms
from flask import flash, redirect, url_for, g
import json

@admin_bp.route('/makeRecurringEvents', methods=['POST'])
def addRecurringEvents():
    recurringEventInfo = request.form.copy()
    recurringEvents = calculateRecurringEventFrequency(recurringEventInfo)
    return json.dumps(recurringEvents)

@admin_bp.route('/<program>/create_event', methods=['GET'])
def createEventPage(program):
    if not g.current_user.isCeltsAdmin:
        abort(403)
    else:
        currentTermid = Term.select().where(Term.isCurrentTerm).get()
        futureTerms = selectFutureTerms(currentTermid)
        eventInfo = ""
        facilitators = getAllFacilitators()
        deleteButton = "hidden"
        endDatePicker = "d-none"
        program = Program.get_by_id(program)

        return render_template("admin/createEvents.html",
                                program = program,
                                futureTerms = futureTerms,
                                facilitators = facilitators,
                                user = g.current_user,
                                deleteButton = deleteButton,
                                endDatePicker = endDatePicker,
                                eventInfo = eventInfo)

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
