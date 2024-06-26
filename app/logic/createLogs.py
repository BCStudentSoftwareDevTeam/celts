from flask import g
from datetime import datetime
from app.models.activityLog import ActivityLog
from app.models.eventRsvpLog import EventRsvpLog
from app.models.adminLog import AdminLog

def createRsvpLog(eventId, content):
    date = datetime.now()
    EventRsvpLog.create(createdBy=g.current_user,createdOn=date,rsvpLogContent=content,event_id=eventId)

def createActivityLog(content):
    date = datetime.now()
    ActivityLog.create(createdBy=g.current_user,createdOn=date,logContent=content)

def createAdminLog(content):
    date = datetime.now()
    AdminLog.create(createdBy=g.current_user,createdOn=date,logContent=content)
