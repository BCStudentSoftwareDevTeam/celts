from flask import Blueprint

# Blueprint Configuration
serviceLearning_bp = Blueprint(
    'serviceLearning', __name__,
    template_folder='templates',
    static_folder='static'
)

from app.controllers.serviceLearning import routes
