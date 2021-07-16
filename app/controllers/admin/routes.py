from flask import request, render_template
from flask import Flask, redirect, flash, url_for
from app.models.event import Event
import json
import datetime
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.logic.updateTrackHours import updateTrackHours

@admin_bp.route('/testing', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/<programID>/<eventID>/track_hours', methods=['GET'])
def trackVolunteerHoursPage(programID, eventID):
    eventParticipantsData = (EventParticipant.select(EventParticipant)
                                .join(Event)
                                .where((EventParticipant.event == eventID) & (Event.program == programID)))
    eventParticipantsData = eventParticipantsData.objects()

    return render_template("/events/trackVolunteerHours.html",
                            eventParticipantsData = list(eventParticipantsData) )

@admin_bp.route('/<programID>/<eventID>/track_hours', methods=['POST'])
def updateHours(programID, eventID):
    updateTrackHours(request.form)
    return redirect(url_for("admin.trackVolunteerHoursPage", programID=programID, eventID=eventID))
