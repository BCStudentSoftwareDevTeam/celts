from flask import request, render_template, g
from flask import Flask, redirect, flash
from app.controllers.events import events_bp
from app.logic.events import groupingEvents
from app.logic.getUpcomingEvents import getUpcomingEventsForUser

@events_bp.route('/events/<term>/', methods=['GET'])
def events(term):
    (studentLedEvents, studentLedPrograms, trainingEvents, trainingPrograms,
    bonnerScholarsEvents, bonnerScholarsPrograms, oneTimeEvents, oneTimePrograms, termName) = groupingEvents(term)

    return render_template("/events/event_list.html",
        studentLedEvents = studentLedEvents,
        studentLedPrograms = studentLedPrograms,
        trainingEvents = trainingEvents,
        trainingPrograms = trainingPrograms,
        bonnerScholarsEvents = bonnerScholarsEvents,
        bonnerScholarsPrograms = bonnerScholarsPrograms,
        oneTimeEvents = oneTimeEvents,
        oneTimePrograms = oneTimePrograms,
        termName = termName,
        user="ramsayb2")


@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)
