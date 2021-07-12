from flask import request, render_template
from flask import Flask, redirect, flash
from app.controllers.admin.createEvents import createEvent
from app.models.program import Program
from app.models.event import Event
from app.models.term import Term
from app.controllers.admin import admin_bp
from app.logic.getAllFacilitators import getAllFacilitators
from flask import g

@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/<program>/create_event', methods=['GET'])
def createEventPage(program):
    listOfTerms = Term.select()
    eventInfo = ""
    facilitators = getAllFacilitators()
    
    try:
        program = Program.get_by_id(program)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            program = program,
                            listOfTerms = listOfTerms,
                            facilitators = facilitators,
                            eventInfo = eventInfo)

@admin_bp.route('/<program>/<eventId>/edit_event', methods=['GET'])
def editEvent(program, eventId):

    facilitators = getAllFacilitators()
    listOfTerms = Term.select()
    eventInfo = Event.get_by_id(eventId)

    isRecurring = "Checked" if eventInfo.isRecurring else ""
    isPrerequisiteForProgram = "Checked" if eventInfo.isPrerequisiteForProgram else ""
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
                            isRecurring = isRecurring,
                            isPrerequisiteForProgram = isPrerequisiteForProgram,
                            isTraining = isTraining,
                            isRsvpRequired = isRsvpRequired,
                            isService = isService)
