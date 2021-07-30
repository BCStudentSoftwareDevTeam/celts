from flask import Flask, redirect, flash, g, url_for, abort
from flask import request, render_template
from app.models.program import Program
from app.models.user import User
from app.models.term import Term
from app.models.eventParticipant import EventParticipant
from app.models.outsideParticipant import OutsideParticipant
from app.models.event import Event
from app.controllers.admin.createEvents import selectFutureTerms
from app.models.programEvent import ProgramEvent
from app.models.facilitator import Facilitator
from app.logic.getAllFacilitators import getAllFacilitators
from app.logic.updateVolunteers import getEventLengthInHours
from app.controllers.admin import admin_bp, getStudent
from app.controllers.admin.deleteEvent import deleteEvent
from app.controllers.admin.createEvents import createEvent
from app.controllers.admin.changeVolunteer import getVolunteers


@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/search_student', methods=['GET'])
def studentSearchPage():
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff:
        return render_template("/searchStudentPage.html")
    abort(403)

@admin_bp.route('/<programID>/<eventID>/track_volunteers', methods=['GET'])
def trackVolunteersPage(programID, eventID):
    if g.current_user.isCeltsAdmin:
        if ProgramEvent.get_or_none(ProgramEvent.event == eventID, ProgramEvent.program == programID):
            eventParticipantsData = EventParticipant.select().where(EventParticipant.event == eventID)

            eventParticipantsData = eventParticipantsData.objects()

            event = Event.get_by_id(eventID)
            program = Program.get_by_id(programID)

            eventLengthInHours = getEventLengthInHours(event.timeStart, event.timeEnd,  event.startDate)


            return render_template("/events/trackVolunteers.html",
                                    eventParticipantsData = list(eventParticipantsData),
                                    eventLength = eventLengthInHours,
                                    program = program,
                                    event = event)
        else:
            raise Exception("Event ID and Program ID mismatched")

    else:
        abort(403)

@admin_bp.route('/<program>/create_event', methods=['GET'])
def createEventPage(program):

    currentTermid = Term.select().where(Term.isCurrentTerm).get()
    futureTerms = selectFutureTerms(currentTermid)
    listOfTerms = Term.select()
    eventInfo = ""
    facilitators = getAllFacilitators()
    deleteButton = "hidden"
    endDatePicker = "d-none"
    try:
        program = Program.get_by_id(program)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            program = program,
                            futureTerms = futureTerms,
                            listOfTerms = listOfTerms,
                            facilitators = facilitators,
                            deleteButton = deleteButton,
                            endDatePicker = endDatePicker,
                            eventInfo = eventInfo)

@admin_bp.route('/<program>/<eventId>/edit_event', methods=['GET'])
def editEvent(program, eventId):

    facilitators = getAllFacilitators()
    listOfTerms = Term.select()
    eventInfo = Event.get_by_id(eventId)
    currentFacilitator = Facilitator.get_or_none(Facilitator.event == eventId)
    deleteButton = "submit"
    hideElement = "hidden"
    isTraining = "Checked" if eventInfo.isTraining else ""
    isRsvpRequired = "Checked" if eventInfo.isRsvpRequired else ""
    isService = "Checked" if eventInfo.isService else ""
    try:
        program = Program.get_by_id(program)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            program = program,
                            currentFacilitator = currentFacilitator,
                            facilitators = facilitators,
                            listOfTerms = listOfTerms,
                            eventInfo = eventInfo,
                            eventId = eventId,
                            isTraining = isTraining,
                            hideElement = hideElement,
                            isRsvpRequired = isRsvpRequired,
                            isService = isService,
                            deleteButton = deleteButton)

@admin_bp.route('/<program>/<eventId>/deleteEvent', methods=['POST'])
def deleteRoute(program, eventId):

    try:
        deleteEvent(program, eventId)
        flash("Event canceled")
        return redirect(url_for("admin.createEventPage", program=program)) #FIXME: Redirect to events page, not create page

    except Exception as e:
        print('Error while canceling event:', e)
        return "", 500
