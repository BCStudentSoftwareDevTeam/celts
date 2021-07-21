from flask import request
from flask import Flask, redirect, flash, g, url_for
from app.models.event import Event
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from app.models.outsideParticipant import OutsideParticipant
from app.models.facilitator import Facilitator
from app.models.programEvent import ProgramEvent

def deleteEvent(program, eventId):
    deleteallInstances = [EventParticipant, Facilitator, OutsideParticipant, ProgramEvent]
    try:

        if Event.get_or_none(Event.id == eventId):
            deleteEvent = Event.get_by_id(eventId)
            deleteEvent.delete_instance(recursive = True, delete_nullable = True)

    except Exception as e:
        #TODO We have to return some sort of error page
        print('Error while canceling event:', e)
        return "", 500
