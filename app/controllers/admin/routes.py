from flask import request, render_template
from flask import Flask, redirect, flash
from app.controllers.admin.createEvents import createEvent
from app.models.program import Program
from app.models.event import Event
from app.models.term import Term
from app.controllers.admin import admin_bp
from app.logic.getAllFacilitators import getAllFacilitators
from app.models.eventParticipant import EventParticipant
from app.models.outsideParticipant import OutsideParticipant
from app.models.facilitator import Facilitator
from flask import g, flash, redirect, url_for
from app.controllers.admin.deleteEvent import deleteEvent

@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/<program>/create_event', methods=['GET'])
def createEventPage(program):
    listOfTerms = Term.select()
    eventInfo = ""
    facilitators = getAllFacilitators()
    deleteButton = "hidden"
    endDatePicker = "d-none"
    try:
        program = Program.get_by_id(program)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            program = program,
                            listOfTerms = listOfTerms,
                            facilitators = facilitators,
                            deleteButton = deleteButton,
                            endDatePicker = endDatePicker,
                            eventInfo = eventInfo)

@admin_bp.route('/<program>/<eventId>/edit_event', methods=['GET'])
def editEvent(program, eventId):

    facilitators = getAllFacilitators()
    listOfTerms = Term.select()
    eventInfo = Event.get_by_id(eventId)
    deleteButton = "submit"
    hideElement = "hidden"
    isTraining = "Checked" if eventInfo.isTraining else ""
    isRsvpRequired = "Checked" if eventInfo.isRsvpRequired else ""
    isService = "Checked" if eventInfo.isService else ""

    try:
        program = Program.get_by_id(program)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            program = program,
                            facilitators = facilitators,
                            listOfTerms = listOfTerms,
                            eventInfo = eventInfo,
                            eventId = eventId,
                            isTraining = isTraining,
                            hideElement = hideElement,
                            isRsvpRequired = isRsvpRequired,
                            isService = isService,
                            deleteButton = deleteButton)

@admin_bp.route('/<program>/<eventId>/deleteEvent', methods=['POST'])
def deleteRoute(program, eventId):

    try:
        deleteEvent(program, eventId)
        flash("Event canceled")
        return redirect(url_for("admin.createEventPage", program=program)) #FIXME: Redirect to events page, not create page

    except Excepttion as e:
        print('Error while canceling event:', e)
        return "", 500
