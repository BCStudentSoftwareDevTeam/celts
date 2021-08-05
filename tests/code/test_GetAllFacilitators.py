import pytest
from app.logic.getAllFacilitators import getAllFacilitators


@pytest.mark.integration
def test_getAllFacilitators():
    userFacilitator = getAllFacilitators()

    assert len(userFacilitator) >= 1
    assert userFacilitator[1].username == 'lamichhanes2'
    assert userFacilitator[1].isFaculty == True
    assert userFacilitator[0].username == "khatts"
    assert userFacilitator[0].isFaculty == False
