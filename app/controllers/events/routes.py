from flask import Flask, redirect, flash, url_for, request, render_template, g, json, abort
from datetime import datetime
from peewee import DoesNotExist

from app.models.term import Term
from app.models.program import Program
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.controllers.events import events_bp
from app.controllers.events import email
from app.logic.emailHandler import EmailHandler
from app.logic.participants import addBnumberAsParticipant

@events_bp.route('/event/<eventid>/kiosk', methods=['GET'])
def loadKiosk(eventid):
    """Renders kiosk for specified event."""
    event = Event.get_by_id(eventid)
    return render_template("/events/eventKiosk.html",
                            event = event,
                            eventid = eventid)

@events_bp.route('/signintoEvent', methods=['POST'])
def kioskSignin():
    """Utilizes form data and sign in function. Returns correct flasher message."""
    eventid = request.form["eventid"]
    bnumber = request.form["bNumber"]

    if not bnumber: # Avoids string index out of range error
        return "", 500

    # scanned bNumber starts with ";" and ends with "?"
    if bnumber[0]==";" and bnumber[-1]=="?": 
        bnumber = "B"+ bnumber[1:9]
    else:
        # regular bnumber with or without a 'B'
        if bnumber[0].isdigit():
            bnumber = "B"+ bnumber[0:8]
        elif bnumber[0].upper() != "B":
            return "", 500
    try:
        kioskUser, userStatus = addBnumberAsParticipant(bnumber, eventid)
        if kioskUser:
            return {"user": f"{kioskUser.firstName} {kioskUser.lastName}", "status": userStatus}
        else:
            return {"user": None, "status": userStatus}

    except Exception as e:
        print("Error in Kiosk Page", e)
        return "", 500
