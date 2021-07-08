import pytest
from app.logic.addRemoveInterest import addRemoveInterest
from peewee import IntegrityError, DoesNotExist

@pytest.mark.integration
def test_addRemoveInterest():
    user = "ramsayb2"
    program_id = 1

    # test adding and removing test cases for different users
    rule = 'addInterest'
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == "Successfully added interest"

    rule = 'deleteInterest'
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'Successfully removed interest'

    rule = 'addInterest'
    user = "khatts"
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'Successfully added interest'

    rule = 'deleteInterest'
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'Successfully removed interest'

    # test add and removing interest with different program id
    rule = 'addInterest'
    program_id = 3
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'Successfully added interest'

    rule = 'deleteInterest'
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == 'Successfully removed interest'

@pytest.mark.integration
def test_addRemoveInvalidInterest():

    program_id = 3

    #test for user that doesn't exist
    user = "al;skfjelh"
    rule = 'addInterest'
    with pytest.raises(IntegrityError):
        addInterest = addRemoveInterest(rule, program_id, user)
        assert addInterest == "Successfully added interest"

    #test removing interest that doesn't exist
    user = "lamichhanes2"
    rule = 'deleteInterest'
    program_id = 2
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == "This interest does not exist"

    # test for incorrect rule
    rule = "lkejfiv"
    addInterest = addRemoveInterest(rule, program_id, user)
    assert addInterest == None
