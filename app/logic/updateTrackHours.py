from flask import request
from app.controllers.admin import admin_bp
# from app.controllers.events import event_bp

from app.models.eventParticipant import EventParticipant

def updateTrackHours(participantData):


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
            except:   #if there is no checkbox for user then they are not preset for the event.
                (EventParticipant.update({EventParticipant.attended: False}).where(EventParticipant.event == participantData['event'],
                    EventParticipant.user == participantData[f'username{user}'])).execute()

                (EventParticipant.update({EventParticipant.hoursEarned: 0}).where(EventParticipant.event == participantData['event'],
                                         EventParticipant.user == participantData[f'username{user}'])).execute()
        else:

            break
