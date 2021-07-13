from flask import request, render_template
from flask import Flask, redirect, flash, g, url_for
from app.models.event import Event
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.models.outsideParticipant import OutsideParticipant
from app.models.facilitator import Facilitator

@admin_bp.route('/<program>/<eventId>/deleteEvent', methods=['POST'])
def deleteEvent(program, eventId):
    try:
        if EventParticipant.get_or_none(EventParticipant.event_id == eventId):
            EventParticipant.get(EventParticipant.event_id == eventId).delete_instance()

        if Facilitator.get_or_none(Facilitator.event_id == eventId):
            Facilitator.get(Facilitator.event_id == eventId).delete_instance()

        if OutsideParticipant.get_or_none(OutsideParticipant.event_id == eventId):
            OutsideParticipant.get(OutsideParticipant.event_id == eventId).delete_instance()

        if Event.get_or_none(Event.id == eventId):
            deleteEvent = Event.get_by_id(eventId)
            deleteEvent.delete_instance()

        flash("Event canceled")
        return redirect(url_for("admin.createEventPage", program=program)) #FIXME: Redirect to events page, not create page

    except Exception as e:
        #TODO We have to return some sort of error page
        print('Error while canceling event:', e)
        return "", 500
