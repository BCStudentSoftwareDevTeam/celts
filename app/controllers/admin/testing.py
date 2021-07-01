import datetime
from app.models.event import Event
from app.models.term import Term
from flask import json, jsonify
from flask import request
from app.controllers.admin import admin_bp
from app.logic.adminCreateEvent import getTermDescription
from app.models.facilitator import Facilitator

@admin_bp.route('/testing_things', methods=['POST'])

def DoSomething():
    rsp = (request.data).decode("utf-8") # This turns byte data into a string
    rspFunctional = json.loads(rsp)

    print(rspFunctional)

    print("Doing Things")
    return ("did something")
