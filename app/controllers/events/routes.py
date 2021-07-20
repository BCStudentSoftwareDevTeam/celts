from flask import request, render_template, g
from flask import Flask, redirect, flash

from app.models.program import Program
from app.controllers.events import events_bp
from app.logic.events import groupingEvents
from app.logic.getUpcomingEvents import getUpcomingEventsForUser

@events_bp.route('/events/<term>/', methods=['GET'])
def events(term):

    studentLedEvents, trainingEvents, bonnerScholarsEvents, oneTimeEvents = groupingEvents(term)
    programs = Program.select()

    return render_template("/events/event_list.html",
            studentLedEvents = studentLedEvents,
            trainingEvents = trainingEvents,
            bonnerScholarsEvents = bonnerScholarsEvents,
            oneTimeEvents = oneTimeEvents,
            user="ramsayb2")
    # if True:
    #     events = studentLedEvents
    # elif False:
    #     events = trainingEvents
    # elif False:
    #     events = bonnerScholarsEvents
    # else:
    #     events = oneTimeEvents
    #
    # return render_template("/events/event_list.html",
    #         events = events,
    #         user="ramsayb2")
@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)
