
from flask import Flask, flash, redirect
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.controllers.events import events_bp
from app.logic.events import getEvents


def sendkioskData(bnumber, eventid):
    # event = Event.get_by_id(eventid)
    bNumberToUser = User.select().where(User.bnumber == bnumber)
    bNumberToUsername = bNumberToUser.objects()[0]
    bNumbertoParticipant = (EventParticipant.update({EventParticipant.attended: True})
                                         .where(EventParticipant.user == bNumberToUsername)
                                         .where(EventParticipant.event == eventid))
    bNumbertoParticipant.execute()
    print("Passed execute")
    return bNumberToUsername
