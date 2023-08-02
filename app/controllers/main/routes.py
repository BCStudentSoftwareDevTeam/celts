from flask import request, render_template, g, abort, flash, redirect, url_for, session
from peewee import JOIN
from playhouse.shortcuts import model_to_dict
import datetime
import json
from http import cookies

from app import app
from app.models.program import Program
from app.models.event import Event
from app.models.backgroundCheck import BackgroundCheck
from app.models.backgroundCheckType import BackgroundCheckType
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.interest import Interest
from app.models.programBan import ProgramBan
from app.models.term import Term
from app.models.eventRsvp import EventRsvp
from app.models.note import Note
from app.models.profileNote import ProfileNote
from app.models.programManager import ProgramManager
from app.models.courseStatus import CourseStatus
from app.models.courseInstructor import CourseInstructor
from app.models.certification import Certification
from app.models.emergencyContact import EmergencyContact
from app.models.insuranceInfo import InsuranceInfo

from app.controllers.main import main_bp
from app.logic.loginManager import logout
from app.logic.users import addUserInterest, removeUserInterest, banUser, unbanUser, isEligibleForProgram, getUserBGCheckHistory, addProfileNote, deleteProfileNote, updateDietInfo
from app.logic.participants import unattendedRequiredEvents, trainedParticipants, getUserParticipatedTrainingEvents, checkUserRsvp, addPersonToEvent
from app.logic.events import *
from app.logic.searchUsers import searchUsers
from app.logic.transcript import *
from app.logic.landingPage import getManagerProgramDict, getActiveEventTab
from app.logic.manageSLFaculty import getCourseDict
from app.logic.courseManagement import unapprovedCourses, approvedCourses
from app.logic.utils import selectSurroundingTerms
from app.logic.certification import getCertRequirementsWithCompletion
from app.logic.serviceLearningCoursesData import saveCourseParticipantsToDatabase,courseParticipantPreviewSessionCleaner
from app.logic.createLogs import createRsvpLog, createAdminLog

@main_bp.route('/logout', methods=['GET'])
def redirectToLogout():
    return redirect(logout())

@main_bp.route('/', methods=['GET'])
def landingPage():
    managerProgramDict = getManagerProgramDict(g.current_user)


    eventsInTerm = list(Event.select().where(Event.term == g.current_term))
    programsWithEventsList = [event.program for event in eventsInTerm if not event.isPast]

    return render_template("/main/landingPage.html", managerProgramDict = managerProgramDict,
                                                     term = g.current_term,
                                                     programsWithEventsList = programsWithEventsList)

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

    term = Term.get_by_id(currentTerm)
    currentEventRsvpAmount = getEventRsvpCountsForTerm(term)
    studentLedEvents = getStudentLedEvents(term)
    trainingEvents = getTrainingEvents(term, g.current_user)
    bonnerEvents = getBonnerEvents(term)
    otherEvents = getOtherEvents(term)

    return render_template("/events/event_list.html",
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
        programID = int(programID))

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
            notes = list(ProgramBan.select(ProgramBan, Note)
                                    .join(Note, on=(ProgramBan.banNote == Note.id))
                                    .where(ProgramBan.user == volunteer,
                                              ProgramBan.program == program,
                                              ProgramBan.endDate > datetime.datetime.now()).execute())

            UserParticipatedTrainingEvents = getUserParticipatedTrainingEvents(program, g.current_user, g.current_term)
            allTrainingsComplete = not len([event for event in UserParticipatedTrainingEvents.values() if event != True])
            noteForDict = notes[-1].banNote.noteContent if notes else ""
            eligibilityTable.append({"program": program,
                                   "completedTraining": allTrainingsComplete,
                                   "trainingList": UserParticipatedTrainingEvents,
                                   "isNotBanned": True if not notes else False,
                                   "banNote": noteForDict})
        profileNotes = ProfileNote.select().where(ProfileNote.user == volunteer)
        userDietQuery = User.select().where(User.username == username)
        userDiet = [note.dietRestriction for note in userDietQuery]

        bonnerRequirements = getCertRequirementsWithCompletion(certification=Certification.BONNER, username=volunteer)
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
                userDiet = userDiet
            )
    abort(403)

@main_bp.route('/profile/<username>/emergencyContact', methods=['GET', 'POST'])
def emergencyContactInfo(username):
    """
    This loads the Emergency Contact Page
    """
    if not (g.current_user.username == username or g.current_user.isCeltsAdmin):
        abort(403)


    if request.method == 'GET':

        # Beans: Q, Should student staff be able to see the emergency contact and insurance info of everyone?
        readOnly = False if g.current_user.username == username else True
        

        contactInfo = EmergencyContact.get_or_none(EmergencyContact.user_id == username)
        return render_template ("/main/emergencyContactInfo.html",
                                username=username,
                                contactInfo=contactInfo,
                                readOnly = readOnly
                                )
    
    elif request.method == 'POST':
        if g.current_user.username != username:
            abort(403)

        contactInfo = EmergencyContact.get_or_none(EmergencyContact.user_id == username)
        if contactInfo:
            contactInfo.update(**request.form).execute()
        else:
            EmergencyContact.create(user = username, **request.form)
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

    if request.method == 'GET':
        # Beans: Q, Should student staff be able to see the emergency contact and insurance info of everyone?
        readOnly = False if g.current_user.username == username else True
        userInsuranceInfo = InsuranceInfo.get_or_none(InsuranceInfo.user == username)
        return render_template ("/main/insuranceInfo.html",
                                username = username,
                                userInsuranceInfo = userInsuranceInfo,
                                readOnly = readOnly
                                )

    # Save the form data
    elif request.method == 'POST':
        if g.current_user.username != username:
            abort(403)

        info = InsuranceInfo.get_or_none(InsuranceInfo.user_id == username)
        if info:
            info.update(**request.form).execute()
        else:
            InsuranceInfo.create(user = username, **request.form)
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
        abort(400)  # Beans: What's the error code for bad user input?
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
        createAdminLog(f'Banned {username} from {programInfo.programName} until {banEndDate}.')
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
        createAdminLog(f'Unbanned {username} from {programInfo.programName}.')
        flash("Successfully unbanned the volunteer", "success")
        return "Successfully unbanned the volunteer"

    except Exception as e:
        print("Error  while updating Unban", e)
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
    allEventTranscript = getAllEventTranscript(username)
    startDate = getStartYear(username)

    return render_template('main/serviceTranscript.html',
                            allEventTranscript = allEventTranscript,
                            slCourses = slCourses.objects(),
                            totalHours = totalHours,
                            startDate = startDate,
                            userData = user)

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

@main_bp.route('/proposalReview/', methods = ['GET', 'POST'])
def reviewProposal():
    """
    this function gets the submitted course id and returns the its data to the review proposal modal
    """
    courseID=request.form
    course=Course.get_by_id(courseID["course_id"])
    instructors_data=course.courseInstructors
    return render_template('/main/reviewproposal.html',
                            course=course,
                            instructors_data=instructors_data)

@main_bp.route('/manageServiceLearning', methods = ['GET', 'POST'])
@main_bp.route('/manageServiceLearning/<term>', methods = ['GET', 'POST'])
def getAllCourseInstructors(term=None):
    """
    This function selects all the Instructors Name and the previous courses
    """
    showPreviewModal = request.args.get('showPreviewModal', default=False, type=bool)
    
    if showPreviewModal and 'courseParticipantPreview' in session:
        courseParticipantPreview = session['courseParticipantPreview']
    else:
        courseParticipantPreview = []

    errorFlag = session.get('errorFlag')
    previewParticipantDisplayList = session.get('previewCourseDisplayList')

    if g.current_user.isCeltsAdmin:
        setRedirectTarget(request.full_path)
        courseDict = getCourseDict()
        term = Term.get_or_none(Term.id == term) or g.current_term

        unapproved = unapprovedCourses(term)
        approved = approvedCourses(term)
        terms = selectSurroundingTerms(g.current_term)

        if request.method =='POST' and "submitParticipant" in request.form:
            saveCourseParticipantsToDatabase(session['courseParticipantPreview'])
            courseParticipantPreviewSessionCleaner()
            flash('File saved successfully!', 'success')
            return redirect(url_for('main.getAllCourseInstructors'))
      
        return render_template('/main/manageServiceLearningFaculty.html',
                                courseInstructors = courseDict,
                                unapprovedCourses = unapproved,
                                approvedCourses = approved,
                                terms = terms,
                                term = term,
                                CourseStatus = CourseStatus, 
                                previewParticipantsErrorFlag = errorFlag,
                                courseParticipantPreview= courseParticipantPreview,
                                previewParticipantDisplayList = previewParticipantDisplayList
                                )
    else:
        abort(403) 

def getRedirectTarget(popTarget=False):
    """
    This function returns a string with the URL or route to a page in the Application
        saved with setRedirectTarget() and is able to pop the value from the session
        to make it an empty value
    popTarget: expects a bool value to determine whether or not to reset
                redirectTarget to an emtpy value
    return: a string with the URL or route to a page in the application that was
            saved in setRedirectTarget()
    """
    if "redirectTarget" not in session:
        return ''

    target = session["redirectTarget"]
    if popTarget:
        session.pop("redirectTarget")
    return target

def setRedirectTarget(target):
    """
    This function saves the target URL in the session for future redirection
        to said page
    target: expects a string that is a URL or a route to a page in the application
    return: None
    """
    session["redirectTarget"] = target

@main_bp.route('/updateDietInformation', methods = ['GET', 'POST'])
def getDietInfo():
    dietaryInfo = request.form
    user = dietaryInfo["user"]
    dietInfo = dietaryInfo["dietInfo"]
    if (g.current_user.username == user) or g.current_user.isAdmin:
        updateDietInfo(user, dietInfo)

    return " "
