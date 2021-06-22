from app.models.event import Event
from flask import json, jsonify
from flask import request

@admin_bp.route('/createEvents', methods=['POST'])
def createEvents():

    rsp = (request.data).decode("utf-8")  # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    all_forms = []

    eventEntry = Event.create(eventName = ,
                              term_id = ,
                              description= ,
                              timeStart = ,
                              timeEnd= ,
                              location = ,
                              isRecurring = ,
                              isRequiredForProgram = ,
                              isService=,
                              startDate= ,
                              endDate= ,
                              files = ,

    )

    #what do we pass

    #how to get value from js

    #add to event table in database
