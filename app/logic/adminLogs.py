from flask import g
from datetime import datetime
from app.models.user import User
from app.models.adminLogs import AdminLogs

def createLog(content):
    date = datetime.now()
    print("This  is the date",date)
    entry = AdminLogs.create(createdBy=g.current_user,createdOn=date,logContent=content)
    entry.save()
