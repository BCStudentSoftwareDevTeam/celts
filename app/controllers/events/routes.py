from flask import request, render_template, g
from flask import Flask, redirect, flash
from app.controllers.events import events_bp
from app.models.term import Term
from app.logic.events import groupEventsByCategory
from app.logic.getUpcomingEvents import getUpcomingEventsForUser

@events_bp.route('/events/<term>/', methods=['GET'])
def events(term):
    # (studentLedEvents, studentLedPrograms, trainingEvents, trainingPrograms,
    # bonnerScholarsEvents, bonnerScholarsPrograms, oneTimeEvents, oneTimePrograms, termName) = groupingEvents(term)

    eventsDict = groupEventsByCategory(term)
    print(eventsDict)
    termName = Term.get_by_id(term).description
    # print(eventsDict.get("Trainings").keys())
    # (key for key, vals in eventsDict.items() if item in vals)
    return render_template("/events/event_list.html",
        studentLedEvents = eventsDict.get("Student Led Event"),
        studentLedPrograms = eventsDict.get("Student Led Event").keys(),
        trainingEvents = eventsDict.get("Trainings"),
        trainingPrograms = eventsDict.get("Trainings").keys(),
        bonnerScholarsEvents = eventsDict.get("Bonner Scholars"),
        bonnerScholarsPrograms = eventsDict.get("Bonner Scholars").keys(),
        oneTimeEvents = eventsDict.get("One Time Events"),
        oneTimePrograms = eventsDict.get("One Time Events").keys(),
        termName = termName,
        user="ramsayb2")


@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)
