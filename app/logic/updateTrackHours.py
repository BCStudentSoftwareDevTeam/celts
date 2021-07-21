from flask import request, flash
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant
from datetime import datetime


def eventLengthInHours(startTime, endTime, eventDate):

    #can only subtract datetime objects, not time objects. So convert time into datetime
    eventLength = datetime.combine(eventDate, endTime) - datetime.combine(eventDate, startTime)
    (h, m, s) = str(eventLength).split(':')
    decimalEventLength = int(h) + round(int(m) / 60, 2)

    return decimalEventLength


def updateTrackHours(participantData):
    """
    updates the events participant table with data from the track hours webpage

    param: participantData- a dictionary that contains data from every row of the page along with the associated username.
    """

    for user in range(1, len(participantData)):
        if f'username{user}' in participantData:
            username = participantData[f'username{user}']
            try:
                if participantData['checkbox_'+ username] == "on": #if the user is marked as present
                    (EventParticipant.update({EventParticipant.hoursEarned: float(participantData['inputHours_'+ username])}).where(EventParticipant.event == participantData['event'],
                                             EventParticipant.user == participantData[f'username{user}'])).execute()

                    (EventParticipant.update({EventParticipant.attended: True}).where(EventParticipant.event == participantData['event'],
                                             EventParticipant.user == participantData[f'username{user}'])).execute()
            except:   #if there is no checkbox for user then they are not present for the event.
                (EventParticipant.update({EventParticipant.attended: False}).where(EventParticipant.event == participantData['event'],
                    EventParticipant.user == participantData[f'username{user}'])).execute()

                (EventParticipant.update({EventParticipant.hoursEarned: 0}).where(EventParticipant.event == participantData['event'],
                                         EventParticipant.user == participantData[f'username{user}'])).execute()
        else:

            break
    flash("Volunteer table successfully updated!")



@admin_bp.route('/addVolunteerToEvent/<user>/<volunteerEventID>', methods = ['POST'])
def addVolunteerToEvent(user, volunteerEventID):
    '''
    Adds a volunteer to the eventparticipant table database after a search and click to 'Add participant' button
    param: user- string containing first name, last name, and username (format: "<firstName> <lastName> (<username>)")
    '''
    try:
        user = user.strip("()")
        userName=user.split('(')[-1]

        alreadyVolunteered = (EventParticipant.select().where(EventParticipant.user==userName, EventParticipant.event==volunteerEventID)).exists()
        if alreadyVolunteered:
            # flash("Volunteer already exists.")
            return("Volunteer already exists.")
        else:
            EventParticipant.create(user=userName, event = volunteerEventID, attended = True)
            # flash('Volunteer successfully added!')
            return "Volunteer successfully added!"

    except Exception as e:
        # flash("Error when adding volunteer")
        return "Error when adding volunteer", 500
