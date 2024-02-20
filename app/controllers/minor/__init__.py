from flask import Blueprint

minor_bp = Blueprint(
    'minor', __name__, 
    template_folder = 'templates',
    static_folder = 'static'
)

from app.controllers.minor import routes