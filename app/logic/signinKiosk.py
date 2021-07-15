
from flask import Flask, flash
from app.models.event import Event
from app.models.user import User
from app.controllers.events import events_bp
from app.logic.events import getEvents



@events_bp.route('/<eventid>/signintoKiosk', methods=['POST'])
def signinKiosk(eventid):
    print("")
