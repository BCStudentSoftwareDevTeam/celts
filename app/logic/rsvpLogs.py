from flask import g
from datetime import datetime
from app.models.rsvpLogs import rsvpLogs

def createRsvpLog(rsvpLogContent):
    date = datetime.now()
    entry = rsvpLogs.create(createdBy=g.current_user,createdOn=date,logContent=rsvpLogContent)
    entry.save()
