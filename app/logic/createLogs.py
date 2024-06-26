from flask import g
from datetime import datetime
from app.models.activityLog import ActivityLog
from app.models.eventRsvpLog import EventRsvpLog

def createRsvpLog(eventId, content):
    date = datetime.now()
    EventRsvpLog.create(createdBy=g.current_user,createdOn=date,rsvpLogContent=content,event_id=eventId)

def createActivityLog(content):
    date = datetime.now()
    ActivityLog.create(createdBy=g.current_user,createdOn=date,logContent=content)

