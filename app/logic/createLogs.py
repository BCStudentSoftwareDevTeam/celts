from flask import g
from datetime import datetime
from app.models.adminLog import AdminLog
from app.models.eventRsvpLog import EventRsvpLog

def createRsvpLog(eventId, content):
    date = datetime.now()
    entry = EventRsvpLog.create(createdBy=g.current_user,createdOn=date,rsvpLogContent=content,event_id=eventId)
    entry.save()

def createAdminLog(content):
    date = datetime.now()
    entry = AdminLog.create(createdBy=g.current_user,createdOn=date,logContent=content)
    entry.save()
