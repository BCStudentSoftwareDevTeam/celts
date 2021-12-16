from flask import g
from datetime import datetime
from app.models.user import User
from app.models.adminLogs import AdminLogs


def createLog(content):
    print(".........................................................")
    date = datetime.now().strftime('%Y %m %d %H:%M:%S')
    print("This is the time:.......................................",date)
    user = g.current_user
    entry = AdminLogs.create(createdBy=user,createdOn=date,logContent=content)
    entry.save()
