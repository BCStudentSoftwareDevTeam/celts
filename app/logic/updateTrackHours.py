from flask import request, flash
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant


def updateTrackHours(participantData):

    print(participantData)
    for user in range(1, len(participantData)):
        if f'username{user}' in participantData:
            username = participantData[f'username{user}']
            try:
                if participantData['checkbox_'+ username] == "on":
                    print(participantData['inputHours_'+ username])
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



@admin_bp.route('/addVolunteerToEvent/<user>/<volunteerEventID>', methods = ['POST'])
def addVolunteerToEvent(user, volunteerEventID):
    '''Adds a volunteer to the eventparticipant table database after a search and click to 'Add participant' button'''
    try:
        userName=user.split("(")[1][:-1]
        alreadyVolunteered = (EventParticipant.select().where(EventParticipant.user==userName, EventParticipant.event==volunteerEventID)).exists()
        if alreadyVolunteered:
            flash("Volunteer already exists.")
            return("Volunteer already exists.")
        else:
            EventParticipant.get_or_create(user=userName, event = volunteerEventID)
            flash('Volunteer successfully added!')
            return "Volunteer successfully added!"

    except Exception as e:
        flash("Error when adding volunteer")
        return "Error when adding volunteer", 500
