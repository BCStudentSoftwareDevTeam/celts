import pytest
from app.controllers.main_routes.alterLSF import modifyLSF, adjustLSF, createOverloadForm
from app.models.user import User
from app.models.laborStatusForm import LaborStatusForm
from app.models.notes import Notes
from app.models.adjustedForm import AdjustedForm
from app.models.formHistory import FormHistory
from datetime import date, datetime
from app import app

@pytest.fixture
def setup():
    delete_forms()
    yield

@pytest.fixture
def cleanup():
    yield
    delete_forms()


def delete_forms():
    formHistories = FormHistory.select().where((FormHistory.formID == 2) & (FormHistory.historyType == "Labor Adjustment Form"))
    for form in formHistories:
        AdjustedForm.delete().where(AdjustedForm.adjustedFormID == form.adjustedForm.adjustedFormID).execute()
        form.delete().execute()
    Notes.delete().where(Notes.formID.cast('char').contains("2")).execute()
    FormHistory.delete().where((FormHistory.formID == 2) & (FormHistory.historyType == "Labor Overload Form")).execute()
    #print("FormHistory")


currentUser = User.get(User.userID == 1) # Scott Heggen's entry in User table
lsf = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 2)
fieldsChanged = {'supervisor':{'oldValue':'B12361006', 'newValue':'B12365892','date':'07/21/2020'},
       'weeklyHours':{'oldValue': '10', 'newValue': '12', 'date': '07/21/2020'},
       'position':{'oldValue': 'S61419', 'newValue': 'S61407', 'date': '07/21/2020'},
       'supervisorNotes':{'oldValue':'old notes.', 'newValue':'new notes.'}
       }

fieldsChangedOverload = {'weeklyHours': {'oldValue':'10', 'newValue':'20', 'date': '07/21/2020'}}

fieldsChangedContractHours = {'contractHours':{'oldValue': '40', 'newValue': '60', 'date': '07/21/2020'}}

@pytest.mark.integration
def test_adjustLSF(setup):
    with app.test_request_context():
        fieldName = 'supervisorNotes'
        adjustLSF(fieldsChanged, fieldName, lsf, currentUser)
        assert Notes.get(Notes.notesContents == 'new notes.')

        fieldName = 'supervisor'
        adjustLSF(fieldsChanged, fieldName, lsf, currentUser)
        adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
        assert adjustedForm.oldValue == 'B12361006'
        assert adjustedForm.newValue == 'B12365892'

        fieldName = 'position'
        adjustLSF(fieldsChanged, fieldName, lsf, currentUser)
        adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
        assert adjustedForm.oldValue == 'S61419'
        assert adjustedForm.newValue == 'S61407'

        fieldName = 'weeklyHours'
        adjustLSF(fieldsChanged, fieldName, lsf, currentUser)
        adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
        assert adjustedForm.oldValue == '10'
        assert adjustedForm.newValue == '12'

        # adjusted overload
        adjustLSF(fieldsChangedOverload, fieldName, lsf, currentUser)
        formHistory = FormHistory.get((FormHistory.formID == lsf.laborStatusFormID) &
                                      (FormHistory.historyType == 'Labor Overload Form'))
        adjustedForm = AdjustedForm.get(AdjustedForm.adjustedFormID == formHistory.adjustedForm)
        assert adjustedForm.oldValue == '10'
        assert adjustedForm.newValue == '20'
        assert formHistory.historyType.historyTypeName == 'Labor Overload Form'

        fieldName = 'contractHours'
        adjustLSF(fieldsChangedContractHours, fieldName, lsf, currentUser)
        adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
        assert adjustedForm.oldValue == '40'
        assert adjustedForm.newValue == '60'

@pytest.mark.integration
def test_modifyLSF(setup):
    with app.test_request_context():
        fieldName = 'supervisorNotes'
        modifyLSF(fieldsChanged, fieldName, lsf, currentUser)
        assert lsf.supervisorNotes == 'new notes.'

        fieldName = 'supervisor'
        modifyLSF(fieldsChanged, fieldName, lsf, currentUser)
        assert lsf.supervisor.ID == 'B12365892'

        fieldName = 'position'
        modifyLSF(fieldsChanged, fieldName, lsf, currentUser)
        assert lsf.POSN_CODE == 'S61407'

        fieldName = 'weeklyHours'
        modifyLSF(fieldsChanged, fieldName, lsf, currentUser)
        assert lsf.weeklyHours == 12

        # Modified verload
        modifyLSF(fieldsChangedOverload, fieldName, lsf, currentUser)
        assert lsf.weeklyHours == 20
        formHistory = FormHistory.get((FormHistory.formID == lsf.laborStatusFormID) &
                                      (FormHistory.historyType == 'Labor Overload Form'))
        assert formHistory.historyType.historyTypeName == 'Labor Overload Form'

        fieldName = 'contractHours'
        modifyLSF(fieldsChangedContractHours, fieldName, lsf, currentUser)
        assert lsf.contractHours == 60

@pytest.mark.integration
def test_createOverloadForm(setup):
    with app.test_request_context():
        newWeeklyHours = 20
        # modify lsf overload form
        createOverloadForm(newWeeklyHours, lsf, currentUser)
        assert lsf.weeklyHours == 20
        formHistory = FormHistory.get((FormHistory.formID == lsf.laborStatusFormID) & (FormHistory.historyType == 'Labor Overload Form'))
        assert formHistory.historyType.historyTypeName == 'Labor Overload Form'

        # adjust lsf overload form
        adjustedforms = AdjustedForm.create(fieldAdjusted = 'weeklyHours',
                                            oldValue      = '10',
                                            newValue      = newWeeklyHours,
                                            effectiveDate = datetime.strptime("07/21/2020", "%m/%d/%Y").strftime("%Y-%m-%d"))

        formHistories = FormHistory.create(formID       = lsf.laborStatusFormID,
                                           historyType  = "Labor Adjustment Form",
                                           adjustedForm = adjustedforms.adjustedFormID,
                                           createdBy    = currentUser,
                                           createdDate  = date.today(),
                                           status       = "Pending")

        createOverloadForm(newWeeklyHours, lsf, currentUser, adjustedforms.adjustedFormID, formHistories)
        adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == 'weeklyHours')
        assert adjustedForm.oldValue == '10'
        assert adjustedForm.newValue == '20'
        formHistory = FormHistory.get((FormHistory.formID == lsf.laborStatusFormID) & (FormHistory.historyType == 'Labor Overload Form'))
        assert formHistory.historyType.historyTypeName == 'Labor Overload Form'
