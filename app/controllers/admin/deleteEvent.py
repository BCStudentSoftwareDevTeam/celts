from flask import request
from flask import Flask, redirect, flash, g, url_for
from app.models.event import Event
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.models.outsideParticipant import OutsideParticipant
from app.models.facilitator import Facilitator

def deleteEvent(program, eventId):
    deleteallInstances = [EventParticipant, Facilitator, OutsideParticipant]
    try:
        for instance in deleteallInstances:
            if instance.get_or_none(instance.event_id == eventId):
                instance.get(instance.event_id == eventId).delete_instance()

        if Event.get_or_none(Event.id == eventId):
            deleteEvent = Event.get_by_id(eventId)
            deleteEvent.delete_instance()

    except Exception as e:
        #TODO We have to return some sort of error page
        print('Error while canceling event:', e)
        return "", 500
