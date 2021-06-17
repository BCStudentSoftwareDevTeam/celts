from flask import request, render_template, g
from flask import Flask, redirect, flash

from app.controllers.events import events_bp
from app.logic.events import getEvents
from app.controllers.events.showUpcomingEvents import showUpcomingEvents

@events_bp.route('/events', methods=['GET'])
def events():
    events = getEvents()

    return render_template("/events/event_list.html",
            events=events,
            user="ramsayb2"
            )

@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = showUpcomingEvents(g.current_user.username)
    random_var = "hello"
    return render_template('/events/showUpcomingEvents.html',
                            random_var = random_var,
                            upcomingEvents = upcomingEvents)
