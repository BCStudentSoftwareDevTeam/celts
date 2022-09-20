from collections import defaultdict
from datetime import date

from app.models.bonnerYear import BonnerYear
from app.models.user import User

def getBonnerCohorts():
    """
        Return a dictionary with years as keys and a list of bonner users as values. Returns empty lists for 
        intermediate years, or the last 5 years if there are no older records.
    """
    currentYear = date.today().year
    years = list(BonnerYear.select(BonnerYear, User).join(User).order_by(BonnerYear.year).execute())

    firstYear = years[0].year if len(years) and years[0].year < currentYear-4 else currentYear-4
    cohorts = { year: [] for year in range(firstYear, currentYear+1) }
    for cohort in years:
        cohorts[cohort.year].append(cohort.user)

    return cohorts
