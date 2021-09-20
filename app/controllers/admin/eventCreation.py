from dateutil import parser
from app.models.event import Event
from flask import request, render_template
from app.models.program import Program
from app.models.eventTemplate import EventTemplate
from app.models.term import Term
from app.controllers.admin import admin_bp
from app.logic.events import eventEdit, getAllFacilitators
from app.logic.eventCreation import createNewEvent, setValueForUncheckedBox, calculateRecurringEventFrequency
from app.logic.eventCreation import validateNewEventData
from app.logic.utils import selectFutureTerms
from flask import flash, redirect, url_for, g
import json

@admin_bp.route('/template_select')
def program_picker():
    allprograms = Program.select().order_by(Program.programName)
    visibleTemplates = EventTemplate.select().where(EventTemplate.isVisible==True).order_by(EventTemplate.name)

    return render_template("/events/template_selector.html",
                programs=allprograms,
                templates=visibleTemplates
            )

@admin_bp.route('/event/<templateid>/create')
@admin_bp.route('/event/<templateid>/<programid>/create')
def template_select(templateid, programid=None):
    if not (g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff):
        abort(403)

    program = None
    try:
        template = EventTemplate.get_by_id(templateid)
        if programid:
            program = Program.get_by_id(programid)

    except DoesNotExist as e:
        print("Invalid template or program id:", e)
        flash("There was an error with your selection. Please try again or contact Systems Support.", "danger")
        return redirect(url_for("admin.program_picker"))

    futureTerms = selectFutureTerms(g.current_term)

    eventData = template.templateData
    if program:
        eventData["program"] = program

    return render_template(f"/admin/{template.templateFile}", 
            template = template,
            eventData = eventData,
            futureTerms = futureTerms)




    eventInfo = ""
    facilitators = getAllFacilitators()
    deleteButton = "hidden"
    endDatePicker = "d-none"

    return render_template("/admin/createEvents.html",
                template = template,
                eventData = eventData,
                futureTerms = futureTerms,
                facilitators = facilitators,
                user = g.current_user,
                deleteButton = deleteButton,
                endDatePicker = endDatePicker,
                eventInfo = eventInfo)

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
                flash("Event successfully updated!", "success")
                return redirect(url_for("events.events", term = newEventData['eventTerm']))
        else:
            flash(validationErrorMessage, 'warning')
            return redirect(url_for("admin.createEventPage", program = newEventData['programId']))
