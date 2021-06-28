import datetime
from app.models.event import Event
from app.models.term import Term
from flask import json, jsonify
from flask import request
from app.controllers.admin import admin_bp
from app.logic.adminCreateEvent import getTermDescription
from app.models.facilitator import Facilitator

@admin_bp.route('/createEvents', methods=['POST'])
def createEvents():

    rsp = (request.data).decode("utf-8") # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    term = Term.select(Term.id).where(Term.description == rspFunctional['evTerm'])

    print(rspFunctional['evStartDate'])
    print(rspFunctional['evEndDate'])

    dateStarts = datetime.datetime.strptime(rspFunctional['evStartDate'], "%m/%d/%Y").strftime("%Y-%m-%d")
    dateEnds = datetime.datetime.strptime(rspFunctional['evEndDate'], "%m/%d/%Y").strftime("%Y-%m-%d")

    dateStart = datetime.datetime.strptime(dateStarts, "%Y-%m-%d")
    dateEnd = datetime.datetime.strptime(dateEnds, "%Y-%m-%d")
    print(dateStart)
    print("HI"*500)
    print(type(dateStart))
    print(dateEnd)
    eventEntry = Event.create(eventName = rspFunctional['evName'],
                              term_id = term,
                              description= rspFunctional['evDescription'],
                              timeStart = rspFunctional['evStartTime'],
                              timeEnd= rspFunctional['evEndTime'],
                              location = rspFunctional['evLocation'],
                              isRecurring = rspFunctional['evRecurringEvent'],
                              isRsvpRequired = rspFunctional['evRSVP'],
                              isRequiredForProgram = rspFunctional['evRequiredForProgram'],
                              isService= rspFunctional['evServiceHours'],
                              startDate =   dateStart,
                              endDate =  dateEnd)

    eventID = Event.select(Event.id).where((Event.eventName == rspFunctional['evName']) &
                                           (Event.description == rspFunctional['evDescription']) &
                                           (Event.startDate == rspFunctional['evStartDate']))

    facilitatorEntry = Facilitator.create(user_id = rspFunctional['evFacilitators'],
                                          event_id = eventID )


    return "Successfully add event!"
