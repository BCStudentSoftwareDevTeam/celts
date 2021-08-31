from flask import request, render_template, url_for, g, Flask, redirect, flash, abort, json, jsonify
from app.models.program import Program
from app.models.event import Event
from app.models.facilitator import Facilitator
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.term import Term
from app.models.outsideParticipant import OutsideParticipant
from app.models.eventParticipant import EventParticipant
from app.models.programEvent import ProgramEvent
from app.logic.participants import trainedParticipants
from app.logic.volunteers import getEventLengthInHours
from app.logic.utils import selectFutureTerms
from app.logic.searchVolunteersAndStudents import searchVolunteersAndStudents
from app.logic.events import deleteEvent, getAllFacilitators
from app.controllers.admin import admin_bp
from app.controllers.admin.volunteers import getVolunteers
from app.controllers.admin.eventCreation import createEvent, addRecurringEvents
from datetime import datetime

@admin_bp.route('/<programID>/<eventID>/track_volunteers', methods=['GET'])
def trackVolunteersPage(programID, eventID):

    attendedTraining = trainedParticipants(programID)
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
                                    event = event,
                                    attendedTraining=attendedTraining)
        else:
            raise Exception("Event ID and Program ID mismatched")

    else:
        abort(403)

@admin_bp.route('/<program>/<eventId>/edit_event', methods=['GET'])
def editEvent(program, eventId):
    facilitators = getAllFacilitators()
    eventInfo = Event.get_by_id(eventId)
    currentTermid = Term.select().where(Term.isCurrentTerm).get()
    futureTerms = selectFutureTerms(currentTermid)

    # FIXME: One of the below two should be replaced which one?
    eventFacilitators = Facilitator.select().where(Facilitator.event == eventInfo)
    currentFacilitator = Facilitator.get_or_none(Facilitator.event == eventId)

    isRecurring = "Checked" if eventInfo.isRecurring else ""
    # isPrerequisiteForProgram = "Checked" if eventInfo.isPrerequisiteForProgram else ""
    isTraining = "Checked" if eventInfo.isTraining else ""
    isRsvpRequired = "Checked" if eventInfo.isRsvpRequired else ""
    isService = "Checked" if eventInfo.isService else ""
    userHasRSVPed = EventParticipant.get_or_none(EventParticipant.user == g.current_user, EventParticipant.event == eventInfo)
    deleteButton = "submit"
    hideElement = "hidden"
    program = Program.get_by_id(program)

    currentDate = datetime.now()
    eventDate = datetime.combine(eventInfo.startDate, eventInfo.timeStart)
    isPastEvent = False
    if currentDate >= eventDate:
        isPastEvent = True


    return render_template("admin/createEvents.html",
                            user = g.current_user,
                            isPastEvent = isPastEvent,
                            program = program,
                            currentFacilitator = currentFacilitator,
                            facilitators = facilitators,
                            futureTerms = futureTerms,
                            eventInfo = eventInfo,
                            eventId = eventId,
                            isRecurring = isRecurring,
                            isTraining = isTraining,
                            hideElement = hideElement,
                            isRsvpRequired = isRsvpRequired,
                            isService = isService,
                            eventFacilitators = eventFacilitators,
                            userHasRSVPed = userHasRSVPed,
                            deleteButton = deleteButton)

@admin_bp.route('/<program>/<eventId>/deleteEvent', methods=['POST'])
def deleteRoute(program, eventId):

    try:
        eventTerm = Event.get(Event.id == eventId).term
        deleteEvent(program, eventId)
        flash("Event canceled")
        return redirect(url_for("events.events", term=eventTerm))

    except Exception as e:
        print('Error while canceling event:', e)
        return "", 500

@admin_bp.route('/volunteerProfile', methods=['POST'])
def volunteerProfile():
    volunteerName= request.form.copy()
    username = volunteerName['searchStudentsInput'].strip("()")
    user=username.split('(')[-1]
    return redirect(url_for('main.profilePage', username=user))

@admin_bp.route('/search_student', methods=['GET'])
def studentSearchPage():
    if g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff:
        return render_template("/searchStudentPage.html")
    abort(403)

# FIXME The following two methods need to be consolidated
@admin_bp.route('/searchStudents/<query>', methods = ['GET'])
def searchStudents(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    searchResults = searchVolunteersAndStudents(query)
    return searchResult


@admin_bp.route('/searchVolunteers/<query>', methods = ['GET'])
def searchVolunteers(query):
    '''Accepts user input and queries the database returning results that matches user search'''

    try:
        query = query.strip()
        search = query.upper() + "%"
        results = User.select().where(User.isStudent & User.firstName ** search | User.lastName ** search)
        resultsDict = {}
        for participant in results:
            resultsDict[participant.firstName + " " + participant.lastName] = participant.firstName + " " + participant.lastName
        dictToJSON = json.dumps(resultsDict)
        return dictToJSON
    except Exception as e:
        print(e)
        return "Error Searching Volunteers query", 500

@admin_bp.route('/addParticipants', methods = ['GET'])
def addParticipants():
    '''Renders the page, will be removed once merged with full page'''

    return render_template('addParticipants.html',
                            title="Add Participants")
