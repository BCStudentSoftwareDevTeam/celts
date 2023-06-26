from flask import g
from datetime import datetime
from app.models.eventRsvpLogs import EventRsvpLogs

def createRsvpLog(eventId, content):
    date = datetime.now()
    entry = EventRsvpLogs.create(createdBy=g.current_user,createdOn=date,logContent=content,event_id=eventId)
    entry.save()
