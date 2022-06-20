from flask import Flask, redirect, flash, url_for, request, render_template, g, json
from datetime import datetime
from peewee import DoesNotExist
from urllib.parse import urlparse

from app.models.term import Term
from app.models.program import Program
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from app.controllers.events import events_bp
from app.controllers.events import email
from app.logic.emailHandler import EmailHandler
from app.logic.events import getUpcomingEventsForUser
from app.logic.participants import sendUserData

@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)

@events_bp.route('/email', methods=['POST'])
def email():
    raw_form_data = request.form.copy()
    if "@" in raw_form_data['emailSender']:
        # when people are sending emails as themselves (using mailto) --- Q: are we still going with the mailto option?
        pass
    else:
        url_domain = urlparse(request.base_url).netloc
        mail = EmailHandler(raw_form_data, url_domain, g.current_user)
        mail_sent = mail.send_email()

        if mail_sent:
            message, status = 'Email successfully sent!', 'success'
        else:
            message, status = 'Error sending email', 'danger'
        flash(message, status)
        return redirect(url_for("main.events", selectedTerm = raw_form_data['selectedTerm']))

@events_bp.route('/eventsList/<eventid>/kiosk', methods=['GET'])
def loadKiosk(eventid):
    """Renders kiosk for specified event."""
    event = Event.get_by_id(eventid)
    return render_template("/events/eventKiosk.html",
                            event = event,
                            eventid = eventid)

@events_bp.route('/signintoEvent', methods=['POST'])
def signinEvent():
    """Utilizes form data and sign in function. Returns correct flasher message."""
    eventid = request.form["eventid"]
    bnumber = request.form["bNumber"]
    programid = ProgramEvent.select(ProgramEvent.program).where(ProgramEvent.event == eventid)

    if bnumber[0]==";" and bnumber[-1]=="?": # scanned bNumber starts with ";" and ends with "?"
        bnumber = "B"+ bnumber[1:9]
    else:
        if bnumber[0].isdigit():
            bnumber = "B"+ bnumber[0:8]
        elif bnumber[0].upper() != "B":
            return "", 500
    try:
        kioskUser, userStatus = sendUserData(bnumber, eventid, programid)
        if userStatus == "banned":
            return "", 500

        elif userStatus == "already in":
            flasherMessage = f"{kioskUser.firstName} {kioskUser.lastName} Already Signed In!"
            return flasherMessage

        else:
            flasherMessage = f"{kioskUser.firstName} {kioskUser.lastName} Successfully Signed In!"
            return flasherMessage

    except Exception as e:
        print("Error in Main Page", e)
        return "", 500
