import pytest
from flask import g
from app import app
from app.models.adminLogs import AdminLogs
from app.logic.adminLogs import createLog
from app.models import mainDB
from app.models.user import User

@pytest.mark.integration
def test_createLogs():
    with mainDB.atomic() as transaction:
        g.current_user = User.get_by_id("ramsayb2")
        currentLogsCount = len(list(AdminLogs.select()))
        createLog("This is a test log")
        assert len(list(AdminLogs.select())) == currentLogsCount +1
        transaction.rollback()
