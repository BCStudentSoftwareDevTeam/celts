from app.models import *
class Term(baseModel):
    description = CharField()
    year = IntegerField()
    academicYear = CharField()
    isSummer = BooleanField(default=False)
    isCurrentTerm = BooleanField(default=False)
    termOrder = CharField()

    _cache = None

    @property
    def academicYearStartingTerm(self):
        """
        Saves the term that starts the academic year of the chosen term in a cache
        to avoid doing multiple queries for the same information.
        """
        if self._cache is None:
            if ("Summer" in self.description) or ("Spring" in self.description):
                try:
                    self._cache = Term.select().where(Term.year==self.year-1, Term.description == f"Fall {self.year-1}").get()
                except DoesNotExist:
                    self._cache = self

            else:
                self._cache = self

        return self._cache

    @property
    def isFutureTerm(self):
        """
        checks to see if the term selected is a current Term.
        If not, depending on the year and description, it determines whether it is a future term
        """
        if not self.isCurrentTerm:
            currentTerm = Term.select().where(Term.isCurrentTerm == True).get()
            if currentTerm.year < self.year:
                return True
            elif currentTerm.year > self.year:
                return False
            else:
                if ("Fall" in currentTerm.description):
                    return False
                elif ("Summer" in currentTerm.description) & ("Fall" in self.description):
                    return True
                elif ("Summer" in currentTerm.description) & ("Spring" in self.description):
                    return False
                elif ("Spring" in currentTerm.description):
                    return True
        return False

    @staticmethod
    def convertDescriptionToTermOrder(description):
        semester,year = description.split()
        if semester == "Spring":
            return year + "-1"
        elif semester == "Summer" or semester == "May":
            return year + "-2"
        elif semester ==  "Fall":
            return year + '-3'