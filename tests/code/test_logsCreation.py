import pytest
from flask import g
from app import app
from datetime import datetime
from app.models.adminLog import AdminLog
from app.logic.createLogs import createAdminLog
from app.models import mainDB
from app.models.user import User

@pytest.mark.integration
def test_createLogs():
    with app.app_context():
        with mainDB.atomic() as transaction:
            g.current_user = User.get_by_id('ramsayb2')
            currentLogsCount = len(list(AdminLog.select()))
            createAdminLog("This is a test log 1")
            allLogs = list(AdminLog.select().order_by(AdminLog.createdOn.desc()))
            mostRecentLog = allLogs[0]
            assert mostRecentLog.createdBy == g.current_user
            assert mostRecentLog.logContent == "This is a test log 1"
            assert datetime.strftime(mostRecentLog.createdOn,'%Y-%m-%d') == datetime.strftime(datetime.now(),'%Y-%m-%d')
            assert len(allLogs) == currentLogsCount +1
            transaction.rollback()
