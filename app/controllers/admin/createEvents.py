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

    eventCheckBoxes = ['eventRequiredForProgram','eventRSVP', 'eventServiceHours' ]

    newEventData = request.form.copy() #since request.form returns a immutable dict. we need to copy to change it

    for checkBox in eventCheckBoxes:
        if checkBox not in newEventData:
            newEventData[checkBox] = 0

    print(newEventData['eventRequiredForProgram'])

    term = Term.select(Term.id).where(Term.description == newEventData['eventTerm'])

    eventEntry = Event.create(eventName = newEventData['eventName'],
                              term_id = term,
                              description= newEventData['eventDescription'],
                              timeStart = newEventData['eventStartTime'],
                              timeEnd= newEventData['eventEndTime'],
                              location = newEventData['eventLocation'],
                              isRecurring = newEventData['recurringEvent'],
                              isRsvpRequired = newEventData['eventRSVP'], #rsvp
                              isRequiredForProgram = newEventData['eventRequiredForProgram'],
                              isService= newEventData['eventServiceHours'],
                              startDate =   newEventData['eventStartDate'],
                              endDate =  newEventData['eventEndDate'])

    eventID = Event.select(Event.id).where((Event.eventName == newEventData['eventName']) &
                                           (Event.description == newEventData['eventDescription']) &
                                           (Event.startDate == newEventData['eventStartDate']))

    facilitatorEntry = Facilitator.create(user_id = newEventData['eventFacilitator'],
                                          event_id = eventID )


    return "Successfully add event!"
