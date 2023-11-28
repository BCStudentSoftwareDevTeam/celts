from peewee import fn 
from app import app
from app.models.celtsLabor import CeltsLabor
from app.logic.celtsLabor import updateCeltsLaborFromLsf


# give count of users inside table currently
preScript = CeltsLabor.select(fn.COUNT(CeltsLabor.user))
print(f'Count before running script: {preScript.scalar()}')
# call function to call to LSF and save labor history to db 
updateCeltsLaborFromLsf()

# give count of updated table 
postScript = CeltsLabor.select(fn.COUNT(CeltsLabor.user))
print(f'Count after running script: {postScript.scalar()}')