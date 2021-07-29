from flask import request, render_template, g
from flask import Flask, redirect, flash
from app.controllers.events import events_bp
from app.models.term import Term
from app.logic.events import groupEventsByCategory
from app.logic.getUpcomingEvents import getUpcomingEventsForUser

@events_bp.route('/events/<term>/', methods=['GET'])
def events(term):

    eventsDict = groupEventsByCategory(term)
    print(eventsDict)
    listOfTerms = Term.select()
    termName = Term.get_by_id(term).description

    return render_template("/events/event_list.html",
        eventDict = eventsDict,
        termName = termName,
        listOfTerms = listOfTerms,
        user = g.current_user)


@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)
