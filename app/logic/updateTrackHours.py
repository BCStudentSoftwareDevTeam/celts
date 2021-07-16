from flask import request
from app.controllers.admin import admin_bp
# from app.controllers.events import event_bp

from app.models.eventParticipant import EventParticipant

# @admin_bp.route('/updateTrackHours', methods=['POST'])
# @main.route('/updateTrackHours', methods=['POST'])
def updateTrackHours(data):
    print('hello')
    # newParticipantTrackHoursData =
    print(data)

    print(data)
