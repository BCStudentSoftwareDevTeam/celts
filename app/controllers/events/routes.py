from flask import request, render_template, g
from flask import Flask, redirect, flash

from app.controllers.events import events_bp
from app.logic.events import getEvents
from app.logic.getUpcomingEvents import getUpcomingEventsForUser
from app.logic.updateTrackHours import updateTrackHours


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
