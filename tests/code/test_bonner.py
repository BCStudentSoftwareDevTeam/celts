import pytest
from datetime import date

from app.models import mainDB
from app.models.bonnerYear import BonnerYear
from app.logic.bonner import getBonnerCohorts

@pytest.mark.integration
def test_getBonnerCohorts():

    with mainDB.atomic() as transaction:
        currentYear = date.today().year

        # always have the last 5, at least
        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert list(cohorts.keys()) == [currentYear-4,currentYear-3,currentYear-2,currentYear-1,currentYear]


        BonnerYear.create(user="lamichhanes2", year=currentYear-6)
        cohorts = getBonnerCohorts()
        assert len(cohorts) == 7
        assert len(cohorts[currentYear]) == 0
        assert len(cohorts[currentYear-6]) == 1

        BonnerYear.create(user="lamichhanes2", year=currentYear-5)
        BonnerYear.create(user="lamichhanes2", year=currentYear-4)
        BonnerYear.create(user="lamichhanes2", year=currentYear-2)
        BonnerYear.create(user="lamichhanes2", year=currentYear-1)
        BonnerYear.create(user="ramsayb2", year=currentYear-1)
        BonnerYear.create(user="khatts", year=currentYear-1)
        BonnerYear.create(user="neillz", year=currentYear-1)
        BonnerYear.create(user="neillz", year=currentYear)

        cohorts = getBonnerCohorts()
        assert len(cohorts) == 7
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 1
        assert len(cohorts[currentYear-1]) == 4

        transaction.rollback()
