from flask import request, render_template
from flask import Flask, redirect, flash

from app.controllers.events import events_bp
from app.logic.events import getEvents

@events_bp.route('/events', methods=['GET'])
def events():
    events = getEvents()

    return render_template("events/event_list.html", 
            events=events,
            user="ramsayb2"
            )
