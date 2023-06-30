from flask import g
from datetime import datetime
from app.models.adminLogs import AdminLogs
from app.models.eventRsvpLogs import EventRsvpLogs

def createRsvpLog(eventId, content):
    date = datetime.now()
    entry = EventRsvpLogs.create(createdBy=g.current_user,createdOn=date,rsvpLogContent=content,event_id=eventId)
    entry.save()

def createAdminLog(content):
    date = datetime.now()
    entry = AdminLogs.create(createdBy=g.current_user,createdOn=date,logContent=content)
    entry.save()
