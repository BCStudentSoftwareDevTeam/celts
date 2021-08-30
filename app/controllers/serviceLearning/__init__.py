from flask import Blueprint

# Blueprint Configuration
serviceLearning_bp = Blueprint(
    'serviceLearning', __name__,
    template_folder='templates',
    static_folder='static'
)

from app.controllers.serviceLearning import routes
from app.controllers.serviceLearning import slcProposal
from app.controllers.serviceLearning import slcGuidelines
from app.controllers.serviceLearning import slcQuestionnaire
