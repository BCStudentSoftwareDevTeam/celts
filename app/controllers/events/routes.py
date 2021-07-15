from flask import request, render_template, g
from flask import Flask, redirect, flash

from app.models.program import Program
from app.controllers.events import events_bp
from app.logic.events import groupingEvents
from app.logic.getUpcomingEvents import getUpcomingEventsForUser
from app.models.programCategory import ProgramCategory

@events_bp.route('/events/<term>', methods=['GET'])
def events(term):

    events = groupingEvents(term)
    programs = Program.select()
    programCategoryVar = ProgramCategory.select()


    return render_template("/events/event_list.html",
            events=events,
            programs = programs,
            programCategoryVar = programCategoryVar,
            user="ramsayb2"
            )

@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)
