import pytest
from app.logic.events import groupingEvents
from peewee import DoesNotExist
from app.models.program import Program


@pytest.mark.integration
def test_termDoesNotExist():
    with pytest.raises(DoesNotExist):
        assert 'Fall 2010' in groupingEvents(100)
        assert 'Spring 2018' in groupingEvents(4)

@pytest.mark.integration
def test_correctQuerying():
    assert 'Spring A 2021' in groupingEvents(1)
    assert [] in groupingEvents(2)
    assert [Program.get_by_id(1), Program.get_by_id(2), Program.get_by_id(3)] in groupingEvents(3)
