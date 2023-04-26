import pytest

from app.models import mainDB
from app.models.user import User
from app.models.term import Term
from app.logic.utils import selectSurroundingTerms
from app.logic.userManagement import addCeltsAdmin, removeCeltsAdmin,addCeltsStudentStaff, removeCeltsStudentStaff, changeCurrentTerm, addNextTerm


@pytest.mark.integration
def test_selectSurroundingTerms():
    listOfTerms = selectSurroundingTerms(Term.get_by_id(3))
    assert 10 == len(listOfTerms)

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=0)
    assert [3,4,5,6,7,8,9] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=1)
    assert [2,3,4,5,6,7,8,9] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=-1)
    assert [4,5,6,7,8,9] == [t.id for t in listOfTerms]

def test_changeCurrentTerm():
    # test via g.current_term
    oldTerm = g.current_term
    changeCurrentTerm(2)
    assert g.current_term == 2
    assert not oldTerm

    # test via isCurrentTerm
    oldTerm2 = g.current_term
    newTerm = changeCurrentTerm(1)
    assert newTerm.isCurrentTerm
    assert not oldTerm2 == g.current_term
    assert not oldTerm2.isCurrentTerm

    # reset data back to before test
    changeCurrentTerm(oldTerm)

def test_invalidTermInputs():
    with pytest.raises(DoesNotExist):
        changeCurrentTerm(100)
    with pytest.raises(DoesNotExist):
        changeCurrentTerm("womp")

@pytest.mark.integration
def test_addNextTerm():
    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Summer 2022",year=2022, academicYear= "2021-2022", isSummer=True,isCurrentTerm=True)
        testTerm.save()

        addNextTerm()

        # for the first test,  make sure we're using the db properly
        terms = list(Term.select().order_by(Term.id))
        newTerm = terms[-1]
        assert newTerm.description == "Fall 2022"
        assert newTerm.year == 2022
        assert newTerm.academicYear == "2022-2023"
        assert not newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()


    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Fall 2029",year=2029, academicYear= "2029-2030", isSummer=False,isCurrentTerm=False)
        testTerm.save()

        newTerm = addNextTerm()
        assert newTerm.description == "Spring 2030"
        assert newTerm.year == 2030
        assert newTerm.academicYear == "2029-2030"
        assert not newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()


    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Spring 2022",year=2022, academicYear= "2021-2022", isSummer=False,isCurrentTerm=False)
        testTerm.save()

        newTerm = addNextTerm()
        assert newTerm.description == "Summer 2022"
        assert newTerm.year == 2022
        assert newTerm.academicYear == "2021-2022"
        assert newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()

@pytest.mark.integration
def test_getStartofCurrentAcademicYear():
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

    assert fallTerm.year == 2020
    assert fallTerm.description == "Fall 2020"
    assert fallTerm.academicYear == "2020-2021"
    
    # Case4: current term has no earlier term, just return itself
    newTerm = Term.create(description="Summer 2020", year=2020, academicYear="2019-2020",isSummer=1,isCurrentTerm=0)
    testTerm = newTerm.academicYearStartingTerm

    assert testTerm == newTerm
    newTerm.delete_instance()

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
