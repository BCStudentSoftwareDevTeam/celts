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
from app.logic.events import getUpcomingEventsForUser
from app.logic.getSLInstructorTableData import getProposalData
from app.logic.participants import trainedParticipants
from app.logic.volunteers import getEventLengthInHours
from app.logic.utils import selectFutureTerms
from app.logic.searchStudents import searchVolunteers
from app.logic.events import deleteEvent, getAllFacilitators, getUpcomingEventsForUser
from app.controllers.admin import admin_bp
from app.controllers.admin.volunteers import getVolunteers
from app.controllers.admin.eventCreation import createEvent, addRecurringEvents
from app.controllers.admin import changeSLAction
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

@admin_bp.route('/courseProposals', methods=['GET'])
def createTable():
    courseDict = getProposalData(g.current_user)
    try:
        return render_template("/admin/createSLProposalTable.html",
                                instructor = g.current_user,
                                courseDict = courseDict)
    except Exception as e:
        print('Error while creating table:', e)
        return "", 500


@admin_bp.route('/courseProposals', methods=['GET'])
def createTable():
    courseDict = getProposalData(g.current_user)
    try:
        return render_template("/admin/createSLProposalTable.html",
                                instructor = g.current_user,
                                courseDict = courseDict)
    except Exception as e:
        print('Error while creating table:', e)
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
    searchResults = searchVolunteers(query)
    return json.dumps(searchResults)


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


@admin_bp.route('/profile/<username>', methods=['GET'])
def viewVolunteersProfile(username):
    if g.current_user.isCeltsAdmin:
         upcomingEvents = getUpcomingEventsForUser(username)
         programs = Program.select()
         interests = Interest.select().where(Interest.user == username)
         programBan = ProgramBan.select().where(ProgramBan.user == username)
         interests_ids = [interest.program for interest in interests]
         eventParticipant = EventParticipant.select().where(EventParticipant.user == username)
         # volunteertTraining = trainedParticipants()
         print("-------------------------------------------------------")
         eligibilityTable = []
         for i in programs:
             # print(i.programName, " ", (username in trainedParticipants(i)), " ", isEligibleForProgram(i, username))
             eligibilityTable.append({"program" : i,
                                      "completedTraining" : (username in trainedParticipants(i)),
                                      "isNotBanned" : isEligibleForProgram(i, username)})
         print(eligibilityTable)
         return render_template ("/admin/volunteerProfileView.html",
            programs = programs,
            eventParticipant = eventParticipant,
            interests = interests,
            programBan = programBan,
            interests_ids = interests_ids,
            upcomingEvents = upcomingEvents,
            eligibilityTable = eligibilityTable,
            # volunteertTraining = volunteertTraining,
            # userProfile = g.current_user,
            user = User.get(User.username == username))
    abort(403)
