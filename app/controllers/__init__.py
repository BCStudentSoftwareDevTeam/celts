from app import app
import os
#from app.login_manager import require_login
from  app.models.programManager import ProgramManager
from  app.models.user import User
from flask import g
#@app.context_processor
#def injectGlobalData():
    #currentUser = require_login()
    #lastStaticUpdate = str(max(os.path.getmtime(os.path.join(root_path, f))
    #              for root_path, dirs, files in os.walk('app/static')
    #               for f in files))
    #return {'currentUser': currentUser,
    #        'lastStaticUpdate': lastStaticUpdate}

@app.context_processor
def injectGlobalData():
    isprogramManager = True if list(ProgramManager.select(ProgramManager, User).join(User).where(User.username == g.current_user).execute()) else False 
    return {"isprogramManager" : isprogramManager}


#   user = (User.select(User, EmergencyContact, InsuranceInfo)
#                 .join(EmergencyContact, JOIN.LEFT_OUTER).switch()
#                 .join(InsuranceInfo, JOIN.LEFT_OUTER)
#                 .where(User.username == username).limit(1))