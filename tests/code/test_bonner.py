import pytest
from datetime import date

from app.models import mainDB
from app.models.bonnerYear import BonnerYear
from app.logic.bonner import getBonnerCohorts

@pytest.mark.integration
def test_getBonnerCohorts():

    with mainDB.atomic() as transaction:
        currentYear = date.today().year

        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert len(cohorts[currentYear]) == 0
        assert len(cohorts[currentYear-1]) == 0

        BonnerYear.create(user="lamichhanes2", year=currentYear-6)
        BonnerYear.create(user="lamichhanes2", year=currentYear-5)
        BonnerYear.create(user="lamichhanes2", year=currentYear-4)
        BonnerYear.create(user="lamichhanes2", year=currentYear-3)
        BonnerYear.create(user="lamichhanes2", year=currentYear-2)
        BonnerYear.create(user="lamichhanes2", year=currentYear-1)
        BonnerYear.create(user="ramsayb2", year=currentYear-1)
        BonnerYear.create(user="khatts", year=currentYear-1)
        BonnerYear.create(user="neillz", year=currentYear-1)
        BonnerYear.create(user="neillz", year=currentYear)

        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert len(cohorts[currentYear]) == 1
        assert len(cohorts[currentYear-1]) == 4

        transaction.rollback()
