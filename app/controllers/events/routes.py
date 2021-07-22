from flask import request, render_template, g
from flask import Flask, redirect, flash
from app.models.event import Event
from app.models.program import Program
from app.controllers.events import events_bp
from app.logic.events import groupingEvents
from app.logic.getUpcomingEvents import getUpcomingEventsForUser

@events_bp.route('/events/<term>/', methods=['GET'])
def events(term):

    groupEvents = (Event.select().join(Program).where(Event.term == term).order_by(Event.program))
    studentLedEvents = (Event.select()
                               .join(Program)
                               .where(Program.isStudentLed))

    studentLedPrograms = []
    [studentLedPrograms.append(event.program) for event in studentLedEvents if event.program not in studentLedPrograms]

    trainingEvents = (Event.select()
                           .where(Event.isTraining))

    trainingProgram = [Program.get_by_id(6)]

    bonnerScholarsEvents = (Event.select()
                                   .join(Program)
                                   .where(Program.isBonnerScholars))

    bonnerScholarsPrograms = []
    [bonnerScholarsPrograms.append(event.program) for event in bonnerScholarsEvents if event.program not in bonnerScholarsPrograms]

    oneTimeEvents = (Event.select()
                          .join(Program)
                          .where(Program.isStudentLed == False,
                                 Event.isTraining == False,
                                 Program.isBonnerScholars == False))

    oneTimeProgram = [Program.get_by_id(4)]
    events = Event.select()
    programs = Program.select()

    return render_template("/events/event_list.html",
            programs = programs,
            events = events,
            studentLedEvents = studentLedEvents,
            studentLedPrograms = studentLedPrograms,
            trainingEvents = trainingEvents,
            trainingProgram = trainingProgram,
            bonnerScholarsEvents = bonnerScholarsEvents,
            bonnerScholarsPrograms = bonnerScholarsPrograms,
            oneTimeEvents = oneTimeEvents,
            oneTimeProgram = oneTimeProgram,
            user="ramsayb2")


@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)
