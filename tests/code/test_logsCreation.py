import pytest
from flask import g
from app import app
from datetime import datetime
from app.models.activityLog import ActivityLog
from app.logic.createLogs import createActivityLog
from app.models import mainDB
from app.models.user import User

@pytest.mark.integration
def test_createLogs():
    with app.app_context():
        with mainDB.atomic() as transaction:
            g.current_user = User.get_by_id('ramsayb2')
            currentLogsCount = len(list(ActivityLog.select()))
            createActivityLog("This is a test log 1")
            allLogs = list(ActivityLog.select().order_by(ActivityLog.createdOn.desc()))
            mostRecentLog = allLogs[0]
            assert mostRecentLog.createdBy == g.current_user
            assert mostRecentLog.logContent == "This is a test log 1"
            assert datetime.strftime(mostRecentLog.createdOn,'%Y-%m-%d') == datetime.strftime(datetime.now(),'%Y-%m-%d')
            assert len(allLogs) == currentLogsCount +1
            transaction.rollback()

@pytest.mark.integration
def test_createLogs():
    with app.app_context():
        with mainDB.atomic() as transaction:
            g.current_user = User.get_by_id('ramsayb2')
            currentLogsCount = len(list(ActivityLog.select()))
            createRSLog("This is a test log 2")
            allLogs = list(ActivityLog.select().order_by(ActivityLog.createdOn.desc()))
            mostRecentLog = allLogs[0]
            assert mostRecentLog.createdBy == g.current_user
            assert mostRecentLog.logContent == "This is a test log 1"
            assert datetime.strftime(mostRecentLog.createdOn,'%Y-%m-%d') == datetime.strftime(datetime.now(),'%Y-%m-%d')
            assert len(allLogs) == currentLogsCount +1
            transaction.rollback()
