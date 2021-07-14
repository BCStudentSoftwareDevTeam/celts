from flask import request
from app.controllers.admin import admin_bp
from app.models.eventParticipant import EventParticipant


@admin_bp.route('/updateTrackHours', methods=['POST'])
def updateTrackHours():
    print('hello')
    participantTrackHoursData = request.form.copy()
    # newParticipantTrackHoursData =
    print (participantTrackHoursData)
