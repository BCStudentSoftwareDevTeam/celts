from flask import Flask, redirect, flash, url_for, request, render_template, g, json
from app.models.event import Event
from app.models.user import User
from app.models.programEvent import ProgramEvent
from app.controllers.events import events_bp
from app.logic.events import getEvents
from app.logic.participants import sendUserData
from datetime import datetime
from app.models.eventRsvp import EventRsvp

@events_bp.route('/events/<term>/', methods=['GET'])
def events(term):
    #set term to current term when events page is accessed from the navbar
    if not term.isdigit():
        term = g.current_term

    currentTime = datetime.now()
    eventsDict = groupEventsByCategory(term)
    listOfTerms = Term.select()
    # participantRSVP = EventParticipant.select().where(EventParticipant.user == g.current_user)
    participantRSVP = EventRsvp.select().where(EventRsvp.user == g.current_user)
    rsvpedEventsID = [event.event.id for event in list(participantRSVP)]

    return render_template("/events/event_list.html",
        selectedTerm = Term.get_by_id(term),
        eventDict = eventsDict,
        listOfTerms = listOfTerms,
        rsvpedEventsID = rsvpedEventsID,
        currentTime = currentTime,
        user = g.current_user)

@events_bp.route('/<eventid>/kiosk', methods=['GET'])
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
    if len(bnumber) > 20:
        bnumber = "B"+ bnumber[1:9]
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
