import pytest
from app.logic.addRemoveInterest import addRemoveInterest
from flask import json

@pytest.mark.integration
def test_addRemoveInterest():
    user = "ramsayb2"
    program_id = 1
    rule = 'addInterest'
    addInterest = addRemoveInterest(rule, program_id, user)
    print(addInterest)

    assert addInterest == 'True'

    rule = 'deleteInterest'

    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'True'

    rule = 'addInterest'
    user = "khatts"
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'True'

    rule = 'deleteInterest'
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'True'

    rule = 'addInterest'
    program_id = 3
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'True'

    rule = 'deleteInterest'
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'True'








# def test_interestUpdate(program_id):
#     """
#     This function updates the interest table by adding a new row when a user
#     shows interest in a program
#     """
#     rule = "addInterest"
#     if 'addInterest' in rule:
#         Interest.get_or_create(program = program_id, user= g.current_user.username)
#     else:
#         deleted_interest = Interest.get(Interest.program == program_id and Interest.user == g.current_user.username)
#         deleted_interest.delete_instance()
