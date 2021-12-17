from flask import g
from datetime import datetime
from app.models.user import User
from app.models.adminLogs import AdminLogs


def createLog(content):
    date = datetime.strptime(datetime.now().strftime('%Y %m %d %H:%M:%S'),'%Y %m %d %H:%M:%S')
    entry = AdminLogs.create(createdBy=g.current_user,createdOn=date,logContent=content)
    entry.save()
