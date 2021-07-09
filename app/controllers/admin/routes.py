from flask import request, render_template
from flask import Flask, redirect, flash
from app.controllers.admin.createEvents import createEvents
from app.models.program import Program
from app.models.event import Event
from app.controllers.admin import admin_bp
from app.logic.adminCreateEvent import getTermDescription, getFacilitators, getCurrentTerm
from flask import g

@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/<program_id>/create_event', methods=['GET'])
def createEvent(program_id):
    termDescriptions = getTermDescription()
    eventFacilitator = getFacilitators()
    currentTerm = getCurrentTerm()
    user = g.current_user
    eventInfo = ""

    try:
        program = Program.get_by_id(program_id)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            user = user,
                            program = program,
                            listOfTermDescriptions = termDescriptions,
                            listOfEventFacilitators = eventFacilitator,
                            theCurrentTerm = currentTerm,
                            eventInfo = eventInfo)

@admin_bp.route('/<program_id>/edit_event', methods=['GET'])
def editEvent(program_id):

    eventId = 2
    termDescriptions = getTermDescription()
    eventFacilitator = getFacilitators()
    currentTerm = getCurrentTerm()
    user = g.current_user
    eventInfo = Event.get_by_id(eventId)

    try:
        program = Program.get_by_id(program_id)

    except:
        return render_template(404)
    return render_template("admin/createEvents.html",
                            user = user,
                            program = program,
                            listOfTermDescriptions = termDescriptions,
                            listOfEventFacilitators = eventFacilitator,
                            theCurrentTerm = currentTerm,
                            eventInfo = eventInfo)
