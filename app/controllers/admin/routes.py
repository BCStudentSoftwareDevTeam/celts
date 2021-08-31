from flask import request, render_template, url_for, g, Flask, redirect, flash, abort
from app.models.program import Program
from app.models.event import Event
from app.models.programBan import ProgramBan
from app.models.interest import Interest
from app.logic.events import getUpcomingEventsForUser
from app.models.facilitator import Facilitator
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.term import Term
from app.models.outsideParticipant import OutsideParticipant
from app.models.programEvent import ProgramEvent
from app.logic.trackAttendees import trainedParticipants
from app.logic.updateVolunteers import getEventLengthInHours
from app.logic.getFacilitatorsAndTerms import getAllFacilitators, selectFutureTerms
from app.controllers.main.volunteerRegisterEvents import volunteerRegister
from app.controllers.admin import admin_bp, getStudent
from app.controllers.admin.deleteEvent import deleteEvent
from app.controllers.admin.changeVolunteer import getVolunteers
from app.controllers.admin.createEvents import createEvent, addRecurringEvents
from datetime import datetime

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

@admin_bp.route('/<program>/create_event', methods=['GET'])
def createEventPage(program):
    if not g.current_user.isCeltsAdmin:
        abort(403)
    else:
        currentTermid = Term.select().where(Term.isCurrentTerm).get()
        futureTerms = selectFutureTerms(currentTermid)
        eventInfo = ""
        facilitators = getAllFacilitators()
        deleteButton = "hidden"
        endDatePicker = "d-none"
        program = Program.get_by_id(program)

        return render_template("admin/createEvents.html",
                                program = program,
                                futureTerms = futureTerms,
                                facilitators = facilitators,
                                user = g.current_user,
                                deleteButton = deleteButton,
                                endDatePicker = endDatePicker,
                                eventInfo = eventInfo)

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
        event = Event.get(Event.id == eventId)
        deleteEvent(program, eventId)
        flash("Event canceled")
        return redirect(url_for("events.events", term = eventTerm.term))

    except Exception as e:
        print('Error while canceling event:', e)
        return "", 500



@admin_bp.route('/profile/<username>', methods=['GET'])
def viewVolunteersProfile(username):
    if g.current_user.isCeltsAdmin:
         upcomingEvents = getUpcomingEventsForUser(username)
         programs = Program.select()
         interests = Interest.select().where(Interest.user == username)
         programban = ProgramBan.select().where(ProgramBan.user == username)
         interests_ids = [interest.program for interest in interests]
         eventParticipant = EventParticipant.select().where(EventParticipant.user == username)
         print("-------------------------------------------------------")
                 # for i in upcomingEvents:
                 #     for j in i.length:
                 #         print(j)
         print(type(eventParticipant))
         return render_template ("/admin/volunteerProfileView.html",
            programs = programs,
            eventParticipant = eventParticipant,
            interests = interests,
            programban = programban,
            interests_ids = interests_ids,
            upcomingEvents = upcomingEvents,
            # userProfile = g.current_user,
            user = User.get(User.username == username))
    abort(403)
