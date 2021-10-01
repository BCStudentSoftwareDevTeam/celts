import pytest
from app.logic.userManagement import addCeltsAdmin, removeCeltsAdmin,addCeltsStudentStaff, removeCeltsStudentStaff
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

def test_addCeltsStudentStaff():
    user = "mupotsal"
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == False
    addCeltsStudentStaff(current_user)
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == True
    removeCeltsStudentStaff(current_user)
    current_user = User.get(User.username == user)
    assert current_user.isCeltsAdmin == False
    
