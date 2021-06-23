from app.models.event import Event
from app.models.term import Term
from flask import json, jsonify
from flask import request
from app.controllers.admin import admin_bp
from app.logic.adminCreateEvent import getTermDescription

@admin_bp.route('/createEvents', methods=['POST'])
def createEvents():

    rsp = (request.data).decode("utf-8") # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    term = Term.select(Term.id).where(Term.description == rspFunctional['evTerm'])
    eventEntry = Event.create(eventName = rspFunctional['evName'],
                              term_id = term,
                              description= rspFunctional['evDescription'],
                              timeStart = rspFunctional['evStartTime'],
                              timeEnd= rspFunctional['evEndTime'],
                              location = rspFunctional['evLocation'],
                              isRecurring = rspFunctional['evRecurringEvent'],
                              isRequiredForProgram = rspFunctional['evRequiredForProgram'],
                              isService= rspFunctional['evServiceHours'],
                              startDate= rspFunctional['evStartDate'],
                              endDate= rspFunctional['evEndDate'],
                              facilitators = rspFunctional['evFacilitators']
     )

    return("it worked!!!!!!!!!! :D")

    #what do we pass

    #how to get value from js

    #add to event table in database
