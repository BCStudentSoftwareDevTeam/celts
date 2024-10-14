import json
import datetime
from peewee import JOIN
from http import cookies
from playhouse.shortcuts import model_to_dict
from flask import request, render_template, jsonify, g, abort, flash, redirect, url_for, make_response, session, request

from app.controllers.main import main_bp
from app import app
from app.models.term import Term
from app.models.user import User
from app.models.note import Note
from app.models.event import Event
from app.models.program import Program
from app.models.interest import Interest
from app.models.eventRsvp import EventRsvp
from app.models.celtsLabor import CeltsLabor
from app.models.programBan import ProgramBan
from app.models.profileNote import ProfileNote
from app.models.insuranceInfo import InsuranceInfo
from app.models.certification import Certification
from app.models.programManager import ProgramManager
from app.models.backgroundCheck import BackgroundCheck
from app.models.emergencyContact import EmergencyContact
from app.models.eventParticipant import EventParticipant
from app.models.courseInstructor import CourseInstructor
from app.models.backgroundCheckType import BackgroundCheckType

from app.logic.events import getUpcomingEventsForUser, getParticipatedEventsForUser, getTrainingEvents, getEventRsvpCountsForTerm, getUpcomingStudentLedCount, getStudentLedEvents, getBonnerEvents, getOtherEvents
from app.logic.transcript import *
from app.logic.loginManager import logout
from app.logic.searchUsers import searchUsers
from app.logic.utils import selectSurroundingTerms
from app.logic.celtsLabor import getCeltsLaborHistory
from app.logic.createLogs import createRsvpLog, createActivityLog
from app.logic.certification import getCertRequirementsWithCompletion
from app.logic.landingPage import getManagerProgramDict, getActiveEventTab
from app.logic.minor import toggleMinorInterest, getCommunityEngagementByTerm, getEngagementTotal
from app.logic.participants import unattendedRequiredEvents, trainedParticipants, getParticipationStatusForTrainings, checkUserRsvp, addPersonToEvent
from app.logic.users import addUserInterest, removeUserInterest, banUser, unbanUser, isEligibleForProgram, getUserBGCheckHistory, addProfileNote, deleteProfileNote, updateDietInfo

@main_bp.route('/logout', methods=['GET'])
def redirectToLogout():
    return redirect(logout())

@main_bp.route('/', methods=['GET'])
def landingPage():

    managerProgramDict = getManagerProgramDict(g.current_user)
    # Optimize the query to fetch programs with non-canceled, non-past events in the current term
  
    programsWithEventsList = list(Program.select(Program, Event)
                                         .join(Event)
                                         .where((Event.term == g.current_term) & (Event.isCanceled == False))
                                         .distinct()
                                         .execute())  # Ensure only unique programs are included
    # Limit returned list to events in the future
    futureEvents = [p for p in programsWithEventsList if not p.event.isPastEnd]

    return render_template("/main/landingPage.html",
                           managerProgramDict=managerProgramDict,
                           term=g.current_term,
                           programsWithEventsList = futureEvents)




@main_bp.route('/goToEventsList/<programID>', methods=['GET'])
def goToEventsList(programID):
    return {"activeTab": getActiveEventTab(programID)}

@main_bp.route('/eventsList/<selectedTerm>', methods=['GET'], defaults={'activeTab': "studentLedEvents", 'programID': 0})
@main_bp.route('/eventsList/<selectedTerm>/<activeTab>', methods=['GET'], defaults={'programID': 0})
@main_bp.route('/eventsList/<selectedTerm>/<activeTab>/<programID>', methods=['GET'])
def events(selectedTerm, activeTab, programID):
    currentTerm = g.current_term
    if selectedTerm:
        currentTerm = selectedTerm
    currentTime = datetime.datetime.now()

    listOfTerms = Term.select()
    participantRSVP = EventRsvp.select(EventRsvp, Event).join(Event).where(EventRsvp.user == g.current_user)
    rsvpedEventsID = [event.event.id for event in participantRSVP]

    term: Term = Term.get_by_id(currentTerm)

    currentEventRsvpAmount = getEventRsvpCountsForTerm(term)
    studentLedEvents = getStudentLedEvents(term)
    countUpcomingStudentLedEvents = getUpcomingStudentLedCount(term, currentTime)
    trainingEvents = getTrainingEvents(term, g.current_user)
    bonnerEvents = getBonnerEvents(term)
    otherEvents = getOtherEvents(term)

    managersProgramDict = getManagerProgramDict(g.current_user)

    # Fetch toggle state from session    
    toggleState = request.args.get('toggleState', 'unchecked')

    # compile all student led events into one list
    studentEvents = []
    for studentEvent in studentLedEvents.values():
        studentEvents += studentEvent # add all contents of studentEvent to the studentEvents list

    # Get the count of all term events for each category to display in the event list page.
    studentLedEventsCount: int = len(studentEvents)
    trainingEventsCount: int = len(trainingEvents)
    bonnerEventsCount: int = len(bonnerEvents)
    otherEventsCount: int = len(otherEvents)

    # gets only upcoming events to display in indicators
    if (toggleState == 'unchecked'):
        studentLedEventsCount: int = sum(list(countUpcomingStudentLedEvents.values()))
        for event in trainingEvents:
            if event.isPastEnd:
                trainingEventsCount -= 1
        for event in bonnerEvents:
            if event.isPastEnd:
                bonnerEventsCount -= 1
        for event in otherEvents:
            if event.isPastEnd:
                otherEventsCount -= 1

    # Handle ajax request for Event category header number notifiers and toggle
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            "studentLedEventsCount": studentLedEventsCount,
            "trainingEventsCount": trainingEventsCount,
            "bonnerEventsCount": bonnerEventsCount,
            "otherEventsCount": otherEventsCount,
            "toggleStatus": toggleState
        })
    
    return render_template("/events/eventList.html",
                            selectedTerm = term,
                            studentLedEvents = studentLedEvents,
                            trainingEvents = trainingEvents,
                            bonnerEvents = bonnerEvents,
                            otherEvents = otherEvents,
                            listOfTerms = listOfTerms,
                            rsvpedEventsID = rsvpedEventsID,
                            currentEventRsvpAmount = currentEventRsvpAmount,
                            currentTime = currentTime,
                            user = g.current_user,
                            activeTab = activeTab,
                            programID = int(programID),
                            managersProgramDict = managersProgramDict,
                            countUpcomingStudentLedEvents = countUpcomingStudentLedEvents,
                            toggleState = toggleState,
                            )

@main_bp.route('/profile/<username>', methods=['GET'])
def viewUsersProfile(username):   
    """
    This function displays the information of a volunteer to the user
    """
    try:
        volunteer = User.get(User.username == username)
    except Exception as e:
        if g.current_user.isAdmin:
            flash(f"{username} does not exist! ", category='danger')
            return redirect(url_for('admin.studentSearchPage'))
        else:
            abort(403)  # Error 403 if non admin/student-staff user trys to access via url

    if (g.current_user == volunteer) or g.current_user.isAdmin: 
        upcomingEvents = getUpcomingEventsForUser(volunteer)
        participatedEvents = getParticipatedEventsForUser(volunteer)
        programs = Program.select()
        if not g.current_user.isBonnerScholar and not g.current_user.isAdmin:
            programs = programs.where(Program.isBonnerScholars == False)
        interests = Interest.select(Interest, Program).join(Program).where(Interest.user == volunteer)
        programsInterested = [interest.program for interest in interests]

        rsvpedEventsList = EventRsvp.select(EventRsvp, Event).join(Event).where(EventRsvp.user == volunteer)
        rsvpedEvents = [event.event.id for event in rsvpedEventsList]

        programManagerPrograms = ProgramManager.select(ProgramManager, Program).join(Program).where(ProgramManager.user == volunteer)
        permissionPrograms = [entry.program.id for entry in programManagerPrograms]

        allBackgroundHistory = getUserBGCheckHistory(volunteer)
        backgroundTypes = list(BackgroundCheckType.select())

        eligibilityTable = []
        
        for program in programs:
            banNotes = list(ProgramBan.select(ProgramBan, Note)
                                    .join(Note, on=(ProgramBan.banNote == Note.id))
                                    .where(ProgramBan.user == volunteer,
                                           ProgramBan.program == program,
                                           ProgramBan.endDate > datetime.datetime.now()).execute())
            userParticipatedTrainingEvents = getParticipationStatusForTrainings(program, [volunteer], g.current_term)
            try:
                allTrainingsComplete = False not in [attended for event, attended in userParticipatedTrainingEvents[username]] # Did volunteer attend all events
            except KeyError:
                allTrainingsComplete = False
            noteForDict = banNotes[-1].banNote.noteContent if banNotes else ""
            eligibilityTable.append({"program": program,
                                     "completedTraining": allTrainingsComplete,
                                     "trainingList": userParticipatedTrainingEvents,
                                     "isNotBanned": (not banNotes),
                                     "banNote": noteForDict})
        profileNotes = ProfileNote.select().where(ProfileNote.user == volunteer)

        bonnerRequirements = getCertRequirementsWithCompletion(certification=Certification.BONNER, username=volunteer)

        managersProgramDict = getManagerProgramDict(g.current_user)
        managersList = [id[1] for id in managersProgramDict.items()]
        totalSustainedEngagements = getEngagementTotal(getCommunityEngagementByTerm(volunteer))

        return render_template ("/main/userProfile.html",
                                programs = programs,
                                programsInterested = programsInterested,
                                upcomingEvents = upcomingEvents,
                                participatedEvents = participatedEvents,
                                rsvpedEvents = rsvpedEvents,
                                permissionPrograms = permissionPrograms,
                                eligibilityTable = eligibilityTable,
                                volunteer = volunteer,
                                backgroundTypes = backgroundTypes,
                                allBackgroundHistory = allBackgroundHistory,
                                currentDateTime = datetime.datetime.now(),
                                profileNotes = profileNotes,
                                bonnerRequirements = bonnerRequirements,
                                managersList = managersList,
                                participatedInLabor = getCeltsLaborHistory(volunteer),
                                totalSustainedEngagements = totalSustainedEngagements,
                            )
    abort(403)

@main_bp.route('/profile/<username>/emergencyContact', methods=['GET', 'POST'])
def emergencyContactInfo(username):
    """
    This loads the Emergency Contact Page
    """
    if not (g.current_user.username == username or g.current_user.isCeltsAdmin):
        abort(403)

    user = User.get(User.username == username)
    
    if request.method == 'GET':
        readOnly = g.current_user.username != username
        contactInfo = EmergencyContact.get_or_none(EmergencyContact.user_id == username)
        return render_template ("/main/emergencyContactInfo.html",
                                username=username,
                                contactInfo=contactInfo,
                                readOnly=readOnly
                                )

    elif request.method == 'POST':
        if g.current_user.username != username:
            abort(403)

        rowsUpdated = EmergencyContact.update(**request.form).where(EmergencyContact.user == username).execute()
        if not rowsUpdated:
            EmergencyContact.create(user = username, **request.form)

        createActivityLog(f"{g.current_user.fullName} updated {user.fullName}'s emergency contact information.")
        flash('Emergency contact information saved successfully!', 'success') 
        
        if request.args.get('action') == 'exit':
            return redirect (f"/profile/{username}")
        else:
            return redirect (f"/profile/{username}/insuranceInfo")

@main_bp.route('/profile/<username>/insuranceInfo', methods=['GET', 'POST'])
def insuranceInfo(username):
    """
    This loads the Insurance Information Page
    """
    if not (g.current_user.username == username or g.current_user.isCeltsAdmin):
            abort(403)
    
    user = User.get(User.username == username)

    if request.method == 'GET':
        readOnly = g.current_user.username != username
        userInsuranceInfo = InsuranceInfo.get_or_none(InsuranceInfo.user == username)
        return render_template ("/main/insuranceInfo.html",
                                username=username,
                                userInsuranceInfo=userInsuranceInfo,
                                readOnly=readOnly
                                )

    # Save the form data
    elif request.method == 'POST':
        if g.current_user.username != username:
            abort(403)

        rowsUpdated = InsuranceInfo.update(**request.form).where(InsuranceInfo.user == username).execute()
        if not rowsUpdated:
            InsuranceInfo.create(user = username, **request.form)

        createActivityLog(f"{g.current_user.fullName} updated {user.fullName}'s insurance information.")
        flash('Insurance information saved successfully!', 'success') 

        if request.args.get('action') == 'exit':
            return redirect (f"/profile/{username}")
        else:
            return redirect (f"/profile/{username}/emergencyContact")

@main_bp.route('/profile/<username>/travelForm', methods=['GET', 'POST'])
def travelForm(username):
    if not (g.current_user.username == username or g.current_user.isCeltsAdmin):
        abort(403)

    user = (User.select(User, EmergencyContact, InsuranceInfo)
                .join(EmergencyContact, JOIN.LEFT_OUTER).switch()
                .join(InsuranceInfo, JOIN.LEFT_OUTER)
                .where(User.username == username).limit(1))
    if not list(user):
        abort(404)
    userData = list(user.dicts())[0]
    userData = {key: value if value else '' for (key, value) in userData.items()}

    return render_template ('/main/travelForm.html',
                            userData = userData
                            )


@main_bp.route('/profile/addNote', methods=['POST'])
def addNote():
    """
    This function adds a note to the user's profile.
    """
    postData = request.form
    try:
        note = addProfileNote(postData["visibility"], postData["bonner"] == "yes", postData["noteTextbox"], postData["username"])
        flash("Successfully added profile note", "success")
        return redirect(url_for("main.viewUsersProfile", username=postData["username"]))
    except Exception as e:
        print("Error adding note", e)
        flash("Failed to add profile note", "danger")
        return "Failed to add profile note", 500

@main_bp.route('/<username>/deleteNote', methods=['POST'])
def deleteNote(username):
    """
    This function deletes a note from the user's profile.
    """
    try:
        deleteProfileNote(request.form["id"])
        flash("Successfully deleted profile note", "success")
    except Exception as e:
        print("Error deleting note", e)
        flash("Failed to delete profile note", "danger")
    return "success"

# ===========================Ban===============================================
@main_bp.route('/<username>/ban/<program_id>', methods=['POST'])
def ban(program_id, username):
    """
    This function updates the ban status of a username either when they are banned from a program.
    program_id: the primary id of the program the student is being banned from
    username: unique value of a user to correctly identify them
    """
    postData = request.form
    banNote = postData["note"] # This contains the note left about the change
    banEndDate = postData["endDate"] # Contains the date the ban will no longer be effective
    try:
        banUser(program_id, username, banNote, banEndDate, g.current_user)
        programInfo = Program.get(int(program_id))
        flash("Successfully banned the volunteer", "success")
        createActivityLog(f'Banned {username} from {programInfo.programName} until {banEndDate}.')
        return "Successfully banned the volunteer."
    except Exception as e:
        print("Error while updating ban", e)
        flash("Failed to ban the volunteer", "danger")
        return "Failed to ban the volunteer", 500

# ===========================Unban===============================================
@main_bp.route('/<username>/unban/<program_id>', methods=['POST'])
def unban(program_id, username):
    """
    This function updates the ban status of a username either when they are unbanned from a program.
    program_id: the primary id of the program the student is being unbanned from
    username: unique value of a user to correctly identify them
    """
    postData = request.form
    unbanNote = postData["note"] # This contains the note left about the change
    try:
        unbanUser(program_id, username, unbanNote, g.current_user)
        programInfo = Program.get(int(program_id))
        createActivityLog(f'Unbanned {username} from {programInfo.programName}.')
        flash("Successfully unbanned the volunteer", "success")
        return "Successfully unbanned the volunteer"

    except Exception as e:
        print("Error while updating Unban", e)
        flash("Failed to unban the volunteer", "danger")
        return "Failed to unban the volunteer", 500


@main_bp.route('/<username>/addInterest/<program_id>', methods=['POST'])
def addInterest(program_id, username):
    """
    This function adds a program to the list of programs a user interested in
    program_id: the primary id of the program the student is adding interest of
    username: unique value of a user to correctly identify them
    """
    try:
        success = addUserInterest(program_id, username)
        if success:
            flash("Successfully added " + Program.get_by_id(program_id).programName + " as an interest", "success")
            return ""
        else:
            flash("Was unable to remove " + Program.get_by_id(program_id).programName + " as an interest.", "danger")

    except Exception as e:
        print(e)
        return "Error Updating Interest", 500

@main_bp.route('/<username>/removeInterest/<program_id>', methods=['POST'])
def removeInterest(program_id, username):
    """
    This function removes a program to the list of programs a user interested in
    program_id: the primary id of the program the student is adding interest of
    username: unique value of a user to correctly identify them
    """
    try:
        removed = removeUserInterest(program_id, username)
        if removed:
            flash("Successfully removed " + Program.get_by_id(program_id).programName + " as an interest.", "success")
            return ""
        else:
            flash("Was unable to remove " + Program.get_by_id(program_id).programName + " as an interest.", "danger")
    except Exception as e:
        print(e)
        return "Error Updating Interest", 500

@main_bp.route('/rsvpForEvent', methods = ['POST'])
def volunteerRegister():
    """
    This function selects the user ID and event ID and registers the user
    for the event they have clicked register for.
    """
    event = Event.get_by_id(request.form['id'])
    program = event.program
    user = g.current_user

    isAdded = checkUserRsvp(user, event)
    isEligible = isEligibleForProgram(program, user)
    listOfRequirements = unattendedRequiredEvents(program, user)

    personAdded = False
    if isEligible:
        personAdded = addPersonToEvent(user, event)
        if personAdded and listOfRequirements:
            reqListToString = ', '.join(listOfRequirements)
            flash(f"{user.firstName} {user.lastName} successfully registered. However, the following training may be required: {reqListToString}.", "success")
        elif personAdded:
            flash("Successfully registered for event!","success")
        else:
            flash(f"RSVP Failed due to an unknown error.", "danger")
    else:
        flash(f"Cannot RSVP. Contact CELTS administrators: {app.config['celts_admin_contact']}.", "danger")


    if 'from' in request.form:
        if request.form['from'] == 'ajax':
            return ''
    return redirect(url_for("admin.eventDisplay", eventId=event.id))

@main_bp.route('/rsvpRemove', methods = ['POST'])
def RemoveRSVP():
    """
    This function deletes the user ID and event ID from database when RemoveRSVP is clicked
    """
    eventData = request.form
    event = Event.get_by_id(eventData['id'])

    currentRsvpParticipant = EventRsvp.get(EventRsvp.user == g.current_user, EventRsvp.event == event)
    logBody = "withdrew from the waitlist" if currentRsvpParticipant.rsvpWaitlist else "un-RSVP'd"
    currentRsvpParticipant.delete_instance()
    createRsvpLog(event.id, f"{g.current_user.fullName} {logBody}.")
    flash("Successfully unregistered for event!", "success")
    if 'from' in eventData:
        if eventData['from'] == 'ajax':
            return ''
    return redirect(url_for("admin.eventDisplay", eventId=event.id))

@main_bp.route('/profile/<username>/serviceTranscript', methods = ['GET'])
def serviceTranscript(username):
    user = User.get_or_none(User.username == username)
    if user is None:
        abort(404)
    if user != g.current_user and not g.current_user.isAdmin:
        abort(403)

    slCourses = getSlCourseTranscript(username)
    totalHours = getTotalHours(username)
    allEventTranscript = getProgramTranscript(username)
    startDate = getStartYear(username)
    return render_template('main/serviceTranscript.html',
                            allEventTranscript = allEventTranscript,
                            slCourses = slCourses.objects(),
                            totalHours = totalHours,
                            startDate = startDate,
                            userData = user)

@main_bp.route('/profile/<username>/removeFromTranscript/<program_id>', methods=['GET'])
def isRemovedFromTranscript(username, program_id):
    user = User.get_or_none(User.username == username)
    if user is None:
        abort(404)

    try:
        bannedProgramsForUser = ProgramBan.get((ProgramBan.program == program_id) & (ProgramBan.user == user))
        # If the user is banned, check if it's marked for removal from transcript
        if bannedProgramsForUser.removeFromTranscript:
            return jsonify({'removedFromTranscript': True})
        else:
            return jsonify({'removedFromTranscript': False})
    except ProgramBan.DoesNotExist:
        return jsonify({'status': 'error', 'message': 'ProgramBan not found'})

@main_bp.route('/profile/<username>/updateTranscript/<program_id>', methods=['POST'])
def updateTranscript(username, program_id):
    # Check user permissions
    user = User.get_or_none(User.username == username)
    if user is None:
        abort(404)
    if user != g.current_user and not g.current_user.isAdmin:
        abort(403)

    # Get the data sent from the client-side JavaScript
    data = request.json

    # Retrieve removeFromTranscript value from the request data
    removeFromTranscript = data.get('removeFromTranscript')

    # Update the ProgramBan object matching the program_id and username
    try:
        bannedProgramsForUser = ProgramBan.get((ProgramBan.program == program_id) & (ProgramBan.user == user))
        bannedProgramsForUser.removeFromTranscript = removeFromTranscript
        bannedProgramsForUser.save()
        return jsonify({'status': 'success'})
    except ProgramBan.DoesNotExist:
        return jsonify({'status': 'error', 'message': 'ProgramBan not found'})


@main_bp.route('/searchUser/<query>', methods = ['GET'])
def searchUser(query):

    category= request.args.get("category")

    '''Accepts user input and queries the database returning results that matches user search'''
    try:
        query = query.strip()
        search = query.upper()
        splitSearch = search.split()
        searchResults = searchUsers(query,category)
        return searchResults
    except Exception as e:
        print(e)
        return "Error in searching for user", 500

@main_bp.route('/contributors',methods = ['GET'])
def contributors():
    return render_template("/contributors.html")

@main_bp.route('/updateDietInformation', methods = ['GET', 'POST'])
def getDietInfo():
    dietaryInfo = request.form
    user = dietaryInfo["user"]
    dietInfo = dietaryInfo["dietInfo"]

    if (g.current_user.username == user) or g.current_user.isAdmin:
        updateDietInfo(user, dietInfo)
        userInfo = User.get(User.username == user)
        if len(dietInfo) > 0:
            createActivityLog(f"Updated {userInfo.fullName}'s dietary restrictions to {dietInfo}.") if dietInfo.strip() else None 
        else:
            createActivityLog(f"Deleted all {userInfo.fullName}'s dietary restrictions dietary restrictions.")


    return " "

@main_bp.route('/profile/<username>/indicateInterest', methods=['POST'])
def indicateMinorInterest(username):
    if g.current_user.isCeltsAdmin or g.current_user.username == username:
        toggleMinorInterest(username)

    else:
        abort(403)
    
    return ""
