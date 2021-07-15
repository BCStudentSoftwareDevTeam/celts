from flask import request, render_template, g
from flask import Flask, redirect, flash
from app.models.event import Event
from app.controllers.events import events_bp
from app.logic.events import getEvents
from app.logic.getUpcomingEvents import getUpcomingEventsForUser
from app.models.user import User

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


@events_bp.route('/<eventid>/Kiosk', methods=['GET'])
def loadKiosk(eventid):
    bnumber = ";007518640202650942826?"
    bnumber = "B"+ bnumber[1:9]
    print(bnumber)
    event = Event.get_by_id(eventid)
    bNumberToUser = User.select(User.username).where(User.bnumber == bnumber)
    print(bNumberToUser)

    return render_template("/events/eventKiosk.html",
                            event = event,
                            bNumberToUser = bNumberToUser,
                            eventid = eventid)
