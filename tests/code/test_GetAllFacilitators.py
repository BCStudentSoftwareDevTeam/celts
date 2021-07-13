import pytest
from app.logic.getAllFacilitators import getAllFacilitators


@pytest.mark.integration
def test_getAllFacilitators():
    userFacilitator = getAllFacilitators()


    assert userFacilitator[0].username == "ramsayb2"
    assert userFacilitator[0].isFaculty == False
