from flask import Flask, redirect, flash, url_for, request, render_template, g, json
from app.models.event import Event
from app.controllers.events import events_bp
from app.logic.events import getEvents
from app.logic.getUpcomingEvents import getUpcomingEventsForUser
from app.models.user import User
from app.logic.signinKiosk import sendkioskData

@events_bp.route('/events', methods=['GET'])
def events():
    events = getEvents()

    return render_template("/events/event_list.html",
            events=events,
            user="ramsayb2"
            )

@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)


@events_bp.route('/<eventid>/kiosk', methods=['GET'])
def loadKiosk(eventid):
    event = Event.get_by_id(eventid)
    return render_template("/events/eventKiosk.html",
                            event = event,
                            eventid = eventid)

@events_bp.route('/signintoKiosk', methods=['POST'])
def signinKiosk():
    """Renders kiosk and calls sign in function. If user already signed in will notify through flasher."""
    eventid = request.form["eventid"]
    bnumber = request.form["bNumber"]

    if len(bnumber) > 20:
        bnumber = "B"+ bnumber[1:9]
    try:
        kioskUser, alreadyIn = sendkioskData(bnumber, eventid)
        if alreadyIn:
            flasherMessage = f"{kioskUser.firstName} {kioskUser.lastName} Already Signed In!"
            return flasherMessage

        else:
            flasherMessage = f"{kioskUser.firstName} {kioskUser.lastName} Successfully Signed In!"
            return flasherMessage

    except Exception as e:
        print("Error in Main Page", e)
        # return "", 500
        flasherMessage = f"See Attendant; Unable to Sign In"
        return flasherMessage
