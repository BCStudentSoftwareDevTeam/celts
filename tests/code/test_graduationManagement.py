import pytest
from flask import json, jsonify
from playhouse.shortcuts import model_to_dict
from app.logic.graduationManagement import setGraduatedStatus

from app.models import mainDB
from app.models.user import User

@pytest.mark.integration
def test_setGraduationStatus():
    with mainDB.atomic() as transaction:
        # Create a user to run the tests with
        testUser = User.create(username = 'usrtst',
                           firstName = 'Test',
                           lastName = 'User',
                           bnumber = '03522492',
                           email = 'usert@berea.deu',
                           hasGraduated = False)
        
        # make sure users have the default values of false and not interested, respectively
        assert testUser.hasGraduated == False
        setGraduatedStatus(testUser.username, 1)
        
        testUser = User.get_by_id(testUser.username)
        # make sure setGraduatedStatus works correctly
        assert testUser.hasGraduated == True
        
        # verify unchecking box will restore defaults
        setGraduatedStatus(testUser.username, 0)
        
        testUser = User.get_by_id(testUser.username)
        assert testUser.hasGraduated == False
        transaction.rollback()