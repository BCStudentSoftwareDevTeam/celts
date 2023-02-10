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
        # reset pre-determined bonner cohorts
        BonnerCohort.delete().execute()

        # make sure it works without specifying the current year    
        currentYear = date.today().year

        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert list(cohorts.keys()) == [currentYear-4,currentYear-3,currentYear-2,currentYear-1,currentYear]

        # always have the last 5, at least
        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert list(cohorts.keys()) == [currentYear-4,currentYear-3,currentYear-2,currentYear-1,currentYear]

        # try a limit greater than our size
        cohorts = getBonnerCohorts(limit=6)
        assert len(cohorts) == 5

        currentYear = 2022 # reset for testing purposes

        BonnerCohort.create(user="lamichhanes2", year=currentYear-6)
        BonnerCohort.create(user="heggens", year=currentYear)
        BonnerCohort.create(user="khatts", year=currentYear)
        cohorts = getBonnerCohorts(currentYear=currentYear)
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

        cohorts = getBonnerCohorts(currentYear=currentYear)
        assert len(cohorts) == 7
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 2
        assert len(cohorts[currentYear-1]) == 4

        cohorts = getBonnerCohorts(limit=5,currentYear=currentYear)
        assert len(cohorts) == 5
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 2
        assert len(cohorts[currentYear-1]) == 4


        transaction.rollback()

@pytest.mark.integration
def test_bonnerRsvp():
    with mainDB.atomic() as transaction:
        # reset pre-determined bonner cohorts
        BonnerCohort.delete().execute()

        BonnerCohort.create(user="lamichhanes2", year=2022)
        BonnerCohort.create(user="ramsayb2", year=2022)
        BonnerCohort.create(user="khatts", year=2020)
        BonnerCohort.create(user="neillz", year=2020)
        event_id = 13

        rsvpForBonnerCohort(2020, event_id)
        assert EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "khatts").exists()
        assert EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "neillz").exists()
        assert not EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "ramsayb2").exists()

        # make sure there is no error for duplicates
        BonnerCohort.create(user="ayisie", year=2020)
        rsvpForBonnerCohort(2020, event_id)
        assert EventRsvp.select().where(EventRsvp.event == event_id).count() == 3

        transaction.rollback()


