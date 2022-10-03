import pytest
from datetime import date

from app.models import mainDB
from app.models.bonnerCohort import BonnerCohort

from app.logic.bonner import getBonnerCohorts

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
        assert len(cohorts[currentYear]) == 0
        assert len(cohorts[currentYear-6]) == 1

        BonnerCohort.create(user="lamichhanes2", year=currentYear-5)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-4)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-2)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-1)
        BonnerCohort.create(user="ramsayb2", year=currentYear-1)
        BonnerCohort.create(user="khatts", year=currentYear-1)
        BonnerCohort.create(user="neillz", year=currentYear-1)
        BonnerCohort.create(user="neillz", year=currentYear)

        cohorts = getBonnerCohorts()
        assert len(cohorts) == 7
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 1
        assert len(cohorts[currentYear-1]) == 4

        cohorts = getBonnerCohorts(limit=5)
        assert len(cohorts) == 5
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 1
        assert len(cohorts[currentYear-1]) == 4


        transaction.rollback()
