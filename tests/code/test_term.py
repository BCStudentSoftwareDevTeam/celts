import pytest
from app.models import mainDB
from app.models.term import Term
from app.logic.utils import selectSurroundingTerms
from app.logic.term import addNextTerm, changeCurrentTerm, addPastTerm

@pytest.mark.integration
def test_selectSurroundingTerms():
    listOfTerms = selectSurroundingTerms(Term.get_by_id(3))
    assert 8 == len(listOfTerms)

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=0)
    assert [3,4,5,6,7,8] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=1)
    assert [2,3,4,5,6,7,8] == [t.id for t in listOfTerms]

    listOfTerms = selectSurroundingTerms(Term.get_by_id(3), prevTerms=-1)
    assert [4,5,6,7,8] == [t.id for t in listOfTerms]

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
        testTerm = Term.create(description="Summer 2022",year=2022, academicYear= "2021-2022", isSummer=True, isCurrentTerm=True, termOrder = Term.convertDescriptionToTermOrder("Summer 2022"))
        testTerm.save()

        addNextTerm()

        terms = list(Term.select().order_by(Term.id))
        newTerm = terms[-1]
        assert newTerm.description == "Summer 2023"
        assert newTerm.year == 2023
        assert newTerm.academicYear == "2022-2023"
        assert newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()

    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Fall 2029",year=2029, academicYear= "2029-2030", isSummer=False,isCurrentTerm=False, termOrder = Term.convertDescriptionToTermOrder("Fall 2029"))
        testTerm.save()

        newTerm = addNextTerm()
        assert newTerm.description == "Spring 2030"
        assert newTerm.year == 2030
        assert newTerm.academicYear == "2029-2030"
        assert not newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()

    with mainDB.atomic() as transaction:
        testTerm = Term.create(description="Spring 2024",year=2022, academicYear= "2023-2024", isSummer=False,isCurrentTerm=False, termOrder = Term.convertDescriptionToTermOrder("Spring 2024") )
        testTerm.save()

        newTerm = addNextTerm()
        assert newTerm.description == "Summer 2024"
        assert newTerm.year == 2024
        assert newTerm.academicYear == "2023-2024"
        assert newTerm.isSummer
        assert not newTerm.isCurrentTerm

        transaction.rollback()
        
@pytest.mark.integration
def test_addPastTerm():
    with mainDB.atomic() as transaction:
        
        assert Term.get_or_none(description = 'Fall 2019') == None
        addPastTerm('Fall 2019')
        testTerm = Term.get_or_none(description = 'Fall 2019')
        assert testTerm.academicYear == '2019-2020'
        assert testTerm.year == 2019
        assert not testTerm.isSummer

        transaction.rollback()
        
    with mainDB.atomic() as transaction:
        assert Term.get_or_none(description = 'Summer 1999') == None
        addPastTerm('Summer 1999')
        testTerm = Term.get_or_none(description = 'Summer 1999')
        assert testTerm.academicYear == '1998-1999'
        assert testTerm.year == 1999
        assert testTerm.isSummer
        
        transaction.rollback()