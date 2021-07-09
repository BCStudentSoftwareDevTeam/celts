from flask import request, render_template
from flask import Flask, redirect, flash

from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant

@admin_bp.route('/testing', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"


@admin_bp.route('/track_hours', methods=['GET'])
def trackVolunteerHoursPage():
    eventParticipantsData = EventParticipant.select()
    return render_template("/events/trackVolunteerHours.html", eventParticipantsData=eventParticipantsData)
