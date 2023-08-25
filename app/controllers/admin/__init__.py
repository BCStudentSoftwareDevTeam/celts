from flask import Blueprint

# Blueprint Configuration
admin_bp = Blueprint(
    'admin', __name__,
    template_folder='templates',
    static_folder='static'
)

from app.controllers.admin import routes
from app.controllers.admin import userManagement 
from app.controllers.admin import volunteers
