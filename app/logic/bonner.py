from collections import defaultdict
from datetime import date

from app.models.bonnerYear import BonnerYear
from app.models.user import User

def getBonnerCohorts():
    """
        Return the last 5 Bonner cohorts
    """
    currentYear = date.today().year
    yearQuery = BonnerYear.select(BonnerYear, User).join(User).where(BonnerYear.year > currentYear-5)

    cohorts = { year: [] for year in range(currentYear-4, currentYear+1) }
    for cohort in yearQuery:
        cohorts[cohort.year].append(cohort.user)

    return cohorts
