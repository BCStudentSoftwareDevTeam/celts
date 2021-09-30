import pytest
from app.logic.userManagement import addCeltsAdmin, removeCeltsAdmin
from app.models.user import User

@pytest.mark.integration
def test_addCeltsAdmin():

    user = "agliullovak"
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == False
    addCeltsAdmin(current_user)
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == True

    removeCeltsAdmin(current_user)
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == False
