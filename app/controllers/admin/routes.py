from flask import request, render_template, abort
from flask import Flask, redirect, flash, url_for
from app.models.event import Event
import json
from datetime import *
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.logic.updateTrackHours import updateTrackHours
from app.logic.trackVolunteerHours import eventLengthInHours
from app.controllers.admin.searchTrackHoursVolunteer import searchTrackHoursVolunteers


@admin_bp.route('/testing', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/<programID>/<eventID>/track_hours', methods=['GET'])
def trackVolunteerHoursPage(programID, eventID):
    eventParticipantsData = (EventParticipant.select(EventParticipant)
                                .join(Event)
                                .where(EventParticipant.event == eventID))

    eventParticipantsData = eventParticipantsData.objects()

    try:

        startTime = eventParticipantsData[0].event.timeStart
        endTime = eventParticipantsData[0].event.timeEnd
        eventDate = eventParticipantsData[0].event.startDate #start date and end date will be the same

        eventLength = eventLengthInHours(startTime, endTime, eventDate)

        program = Program.get_by_id(programID)

        return render_template("/events/trackVolunteerHours.html",
                                eventParticipantsData = list(eventParticipantsData),
                                eventLength = eventLength,
                                program = program)
    except:
        abort(404)


@admin_bp.route('/<programID>/<eventID>/track_hours', methods=['POST'])
def updateHours(programID, eventID):
    updateTrackHours(request.form)
    return redirect(url_for("admin.trackVolunteerHoursPage", programID=programID, eventID=eventID))
