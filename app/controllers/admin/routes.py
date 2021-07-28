from flask import request, render_template, abort, flash
from flask import Flask, redirect, url_for, g
from app.models.event import Event
from app.models.programEvent import ProgramEvent
import json
from datetime import *
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.logic.updateTrackVolunteers import getEventLengthInHours
from app.controllers.admin.changeTrackVolunteer import searchTrackVolunteers
from peewee import DoesNotExist


@admin_bp.route('/testing', methods=['GET'])
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
            startTime = event.timeStart
            endTime = event.timeEnd
            eventDate = event.startDate #start date and end date will be the same

            eventLengthInHours = getEventLengthInHours(startTime, endTime, eventDate)


            return render_template("/events/trackVolunteers.html",
                                    eventParticipantsData = list(eventParticipantsData),
                                    eventLength = eventLengthInHours,
                                    program = program,
                                    event = event)
        else:
            raise Exception("Event ID and Program ID mismatched")

    else:
        abort(403)
