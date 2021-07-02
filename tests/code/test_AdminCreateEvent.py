import pytest
from app.logic.adminCreateEvent import getTermDescription, getCurrentTerm, getFacilitators

@pytest.mark.integration
def test_getTermDescription():
    empty_list =[]
    termDescription = getTermDescription()

    assert type(termDescription) == type(empty_list)

    assert len(termDescription) > 0

    assert(termDescription[2]) == "Summer 2021"





@pytest.mark.integration
def test_getCurrentTerm():
    currentTerm = getCurrentTerm()
    assert (currentTerm) == "Summer 2021"


@pytest.mark.integration
def test_getFacilitators():
    userFacilitator = getFacilitators()


    assert userFacilitator[0].username == "bryanta"
    assert userFacilitator[1].isFaculty == 1
    assert userFacilitator[1].isFaculty == True
