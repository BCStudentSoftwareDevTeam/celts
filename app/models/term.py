from app.models import *
class Term(baseModel):
    description = CharField()
    year = IntegerField()
    academicYear = CharField()
    isSummer = BooleanField(default=False)
    isCurrentTerm = BooleanField(default=False)

    _cache = None

    @property
    def academicYearStartingTerm(self):
        """
        Saves the term that starts the academic year of the chosen term in a cache
        to avoid doing multiple queries for the same information.
        """
        if self._cache is None:
            if ("Summer" in self.description) or ("Spring" in self.description):
                self._cache = Term.select().where(Term.year==self.year-1, Term.description == f"Fall {self.year-1}").get()
            else:
                self._cache = self

        return self._cache
