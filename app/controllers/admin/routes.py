from flask import request, render_template, abort, flash
from flask import Flask, redirect, url_for, g
from app.models.event import Event
from app.models.programEvent import ProgramEvent
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.term import Term
from app.logic.getAllFacilitators import getAllFacilitators
from app.controllers.admin.createEvents import createEvent
from app.logic.updateVolunteers import getEventLengthInHours
from app.controllers.admin.changeVolunteer import getVolunteers


@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/<programID>/<eventID>/track_volunteers', methods=['GET'])
def trackVolunteersPage(programID, eventID):
    if g.current_user.isCeltsAdmin:
        if ProgramEvent.get_or_none(ProgramEvent.event == eventID, ProgramEvent.program == programID):
            eventParticipantsData = EventParticipant.select().where(EventParticipant.event == eventID)

            eventParticipantsData = eventParticipantsData.objects()

            event = Event.get_by_id(eventID)
            program = Program.get_by_id(programID)

            eventLengthInHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)


            return render_template("/events/trackVolunteers.html",
                                    eventParticipantsData = list(eventParticipantsData),
                                    eventLength = eventLengthInHours,
                                    program = program,
                                    event = event)
        else:
            raise Exception("Event ID and Program ID mismatched")

    else:
        abort(403)

@admin_bp.route('/<program>/create_event', methods=['GET'])
def createEventPage(program):
    listOfTerms = Term.select()
    facilitators = getAllFacilitators()
    try:
        program = Program.get_by_id(program)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            program = program,
                            listOfTerms = listOfTerms,
                            facilitators = facilitators)
