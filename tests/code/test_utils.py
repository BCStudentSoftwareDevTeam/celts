import pytest
from types import SimpleNamespace

from app.models import mainDB
from app.models.term import Term
from app.logic.utils import selectAllSummerTerms



@pytest.mark.integration
def test_getStartofCurrentAcademicYear():
    with mainDB.atomic() as transaction:
        # Case1: current term is Fall 2020
        currentTerm = Term.get_by_id(1)
        fallTerm = currentTerm.academicYearStartingTerm
        assert fallTerm.year == 2020
        assert fallTerm.description == "Fall 2020"
        assert fallTerm.academicYear == "2020-2021"

        # Case2: current term is Spring 2021
        currentTerm = Term.get_by_id(2)
        fallTerm = currentTerm.academicYearStartingTerm
        assert fallTerm.year == 2020
        assert fallTerm.description == "Fall 2020"
        assert fallTerm.academicYear == "2020-2021"

        # Case3: current term is Summer 2021
        currentTerm = Term.get_by_id(4)
        fallTerm = currentTerm.academicYearStartingTerm
        assert fallTerm.year == 2021
        assert fallTerm.description == "Fall 2021"
        assert fallTerm.academicYear == "2021-2022"
        
        # Case4: current term has no earlier term, just return itself
        newTerm = Term.create(description="Summer 2020", year=2020, academicYear="2019-2020",isSummer=1,isCurrentTerm=0)
        testTerm = newTerm.academicYearStartingTerm

        assert testTerm == newTerm
        newTerm.delete_instance()
        transaction.rollback()

@pytest.mark.integration
def test_isFutureTerm():
    with mainDB.atomic() as transaction:
        dbCurrentTerm = Term.select().where(Term.isCurrentTerm == True).get()
        dbCurrentTerm.isCurrentTerm = False
        dbCurrentTerm.save()
        testCurrentTerm = Term.create(description = "Summer 1900",
                                    year = 1900,
                                    academicYear = "1899-1900",
                                    isSummer = True,
                                    isCurrentTerm = True)
        sameYearFutureTerm = Term.create(description = "Fall 1900",
                                    year = 1900,
                                    academicYear = "1900-1901",
                                    isSummer = False,
                                    isCurrentTerm = False)
        sameYearPastTerm = Term.create(description = "Spring 1900",
                                    year = 1900,
                                    academicYear = "1899-1900",
                                    isSummer = False,
                                    isCurrentTerm = False)
        futureYearTerm = Term.create(description = "Fall 1901",
                                    year = 1901,
                                    academicYear = "1901-1902",
                                    isSummer = False,
                                    isCurrentTerm = False)
        pastYearTerm = Term.create(description = "Spring 1899",
                                    year = 1899,
                                    academicYear = "1899-1900",
                                    isSummer = False,
                                    isCurrentTerm = False)
        # future term this year
        assert sameYearFutureTerm.isFutureTerm == True
        # future term in future year
        assert futureYearTerm.isFutureTerm == True
        # past term this year
        assert sameYearPastTerm.isFutureTerm == False
        # past term previous year
        assert pastYearTerm.isFutureTerm == False
        # current term
        assert testCurrentTerm.isFutureTerm == False
        transaction.rollback()


@pytest.mark.integration
@pytest.mark.parametrize(
    "class_level, current_description, current_year, expected_years",
    [
        ("Freshman", "Fall 2090", 2090, [2091, 2092, 2093]),
        ("Sophomore", "Summer 2091", 2091, [2090, 2091, 2092]),
        ("Senior", "Fall 2090", 2090, [2088, 2089, 2090]),
    ],
)
def test_selectAllSummerTerms_uses_estimated_enrollment_window(
        class_level, current_description, current_year, expected_years):
    with mainDB.atomic() as transaction:
        for year in range(2087, 2096):
            Term.create(description=f"Summer {year}",
                        year=year,
                        academicYear=f"{year - 1}-{year}",
                        isSummer=True,
                        isCurrentTerm=False,
                        termOrder=f"{year}-2")

        student = SimpleNamespace(rawClassLevel=class_level,
                                  hasGraduated=False)
        currentTerm = SimpleNamespace(description=current_description,
                                      year=current_year)

        assert expected_years == [
            term.year for term in selectAllSummerTerms(currentTerm, student)
        ]
        transaction.rollback()


def test_selectAllSummerTerms_excludes_graduated_students():
    student = SimpleNamespace(rawClassLevel="Senior", hasGraduated=True)
    currentTerm = SimpleNamespace(description="Summer 2090", year=2090)

    assert selectAllSummerTerms(currentTerm, student) == []


def test_selectAllSummerTerms_excludes_unknown_class_levels():
    student = SimpleNamespace(rawClassLevel=None, hasGraduated=False)
    currentTerm = SimpleNamespace(description="Summer 2090", year=2090)

    assert selectAllSummerTerms(currentTerm, student) == []
