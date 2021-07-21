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

    print(studentLedPrograms)

    trainingEvents = (Event.select()
                           .where(Event.isTraining))

    bonnerScholarsEvents = (Event.select()
                                   .join(Program)
                                   .where(Program.isBonnerScholars))

    bonnerScholarPrograms = {event.program_id: event.program.programName for event in bonnerScholarsEvents}


    oneTimeEvents = (Event.select()
                          .join(Program)
                          .where(Program.isStudentLed == False,
                                 Event.isTraining == False,
                                 Program.isBonnerScholars == False))

    oneTimePrograms = {event.program_id: event.program.programName for event in oneTimeEvents}

    print(groupEvents)
    events = Event.select()
    programs = Program.select()

    return render_template("/events/event_list.html",
            programs = programs,
            events = events,
            studentLedEvents = studentLedEvents,
            trainingEvents = trainingEvents,
            bonnerScholarsEvents = bonnerScholarsEvents,
            oneTimeEvents = oneTimeEvents,
            oneTimePrograms = oneTimePrograms,
            bonnerScholarPrograms = bonnerScholarPrograms,
            studentLedPrograms = studentLedPrograms,
            user="ramsayb2")


@events_bp.route('/events/upcoming_events', methods=['GET'])
def showUpcomingEvent():
    upcomingEvents = getUpcomingEventsForUser(g.current_user)
    return render_template('/events/showUpcomingEvents.html',
                            upcomingEvents = upcomingEvents)

#
# {% set category = studentLedPrograms %}
# {% for program in studentLedPrograms %}
# {% set accordion %}
# <div class="accordion" id="accordion_{{program.id}}">
#   <div class="accordion-item">
#     <h2 class="accordion-header" id="accordion__header_{{program.id}}">
#       <button class="accordion-button"
#               type="button"
#               data-bs-toggle="collapse"
#               data-bs-target="#accordion__body_{{program.id}}"
#               aria-expanded="true"
#               aria-controls="accordion__body_{{program.id}}" >
#               {{studentLedPrograms.get(program)}}
#       </button>
#     </h2>
#
#     <div id="accordion__body_{{program.id}}"
#           class="accordion-collapse collapse hide"
#           aria-labelledby="accordion__header_{{program.id}}"
#           data-bs-parent="#accordion_{{program.id}}">
#       <div class="accordion-body">
#         <table class="table table-striped">
#           <thead>
#             <tr>
#               <th scope="col">Event Name</th>
#               <th scope="col">Date</th>
#               <th scope="col">Time</th>
#               <th scope="col">Location</th>
#               <th scope="col">Invitation</th>
#             </tr>
#           </thead>
#           <tbody>
#             <tr>
#               <td> <a href="#" class="link-primary">{{events.description}}</a></td> {# FIXME:change href #}
#               <td>{{events.startDate}}</td>
#               <td>{{events.timeStart}}</td>
#               <td>{{events.location}}</td>
#               <td><button type="button" class="btn btn-warning">Email</button></td>
#             </tr>
#           </tbody>
#         </table>
#       </div>
#     </div>
#   </div>
# </div>
# {% endset %}
# {% endfor %}
