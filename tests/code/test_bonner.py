import pytest
from datetime import date
from peewee import IntegrityError

from app.models import mainDB
from app.models.bonnerCohort import BonnerCohort
from app.models.eventRsvp import EventRsvp

from app.logic.bonner import getBonnerCohorts, rsvpForBonnerCohort

@pytest.mark.integration
def test_getBonnerCohorts():

    with mainDB.atomic() as transaction:
        currentYear = date.today().year

        # reset bonner students
        BonnerCohort.delete().execute()

        # always have the last 5, at least
        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert list(cohorts.keys()) == [currentYear-4,currentYear-3,currentYear-2,currentYear-1,currentYear]

        # try a limit greater than our size
        cohorts = getBonnerCohorts(limit=6)
        assert len(cohorts) == 5


        BonnerCohort.create(user="lamichhanes2", year=currentYear-6)
        cohorts = getBonnerCohorts()
        assert len(cohorts) == 7
        assert len(cohorts[currentYear]) == 2
        assert len(cohorts[currentYear-6]) == 1

        BonnerCohort.create(user="lamichhanes2", year=currentYear-5)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-4)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-2)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-1)
        BonnerCohort.create(user="ayisie", year=currentYear-1)
        BonnerCohort.create(user="khatts", year=currentYear-1)
        BonnerCohort.create(user="heggens", year=currentYear-1)
        BonnerCohort.create(user="khatts", year=currentYear)

        cohorts = getBonnerCohorts()
        assert len(cohorts) == 7
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 3
        assert len(cohorts[currentYear-1]) == 6

        cohorts = getBonnerCohorts(limit=5)
        assert len(cohorts) == 5
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 1
        assert len(cohorts[currentYear-1]) == 4


        transaction.rollback()

@pytest.mark.integration
def test_bonnerRsvp():
    with mainDB.atomic() as transaction:
        BonnerCohort.create(user="lamichhanes2", year=2022)
        BonnerCohort.create(user="ramsayb2", year=2022)
        BonnerCohort.create(user="khatts", year=2020)
        BonnerCohort.create(user="neillz", year=2020)
        event_id = 13

        rsvpForBonnerCohort(2020, event_id)
        assert EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "khatts").exists()
        assert EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "neillz").exists()

        # make sure there is no error for duplicates
        BonnerCohort.create(user="ayisie", year=2020)
        rsvpForBonnerCohort(2020, event_id)
        assert EventRsvp.select().where(EventRsvp.event == event_id).count() == 3

        transaction.rollback()


