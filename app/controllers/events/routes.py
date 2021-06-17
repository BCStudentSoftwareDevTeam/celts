from flask import request, render_template
from flask import Flask, redirect, flash

from app.controllers.events import events_bp
from app.logic.events import getEvents
from app.controllers.showUpcomingEvents import showUpcomingEvents

@events_bp.route('/events', methods=['GET'])
def events():
    events = getEvents()

    return render_template("events/event_list.html",
            events=events,
            user="ramsayb2"
            )

@events_bp.route('/events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = showUpcomingEvents("khatts") #FIXME: use g.current_user when that gets implemented
    return render_template('showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)
