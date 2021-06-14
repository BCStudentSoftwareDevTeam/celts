from flask import Blueprint

# Blueprint Configuration
events_bp = Blueprint(
    'events', __name__,
    template_folder='templates',
    static_folder='static'
)

from app.controllers.events import routes
