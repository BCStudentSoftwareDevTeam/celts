from flask import request, render_template
from flask import Flask, redirect, flash

from app.models.program import Program
from app.controllers.events import events_bp
from app.logic.events import groupingEvents

@events_bp.route('/events/<term>', methods=['GET'])
def events(term):

    events = groupingEvents(term)
    programs = Program.select()
    print(list(programs), "here")
    for event in events:
        print(event.program)

    return render_template("events/event_list.html",
            events=events,
            programs = programs,
            user="ramsayb2"
            )
