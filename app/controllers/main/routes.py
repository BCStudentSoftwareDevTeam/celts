from flask import request, render_template

from app.controllers.main import main_bp

@main_bp.route('/')
def index():
    try:
        return render_template('main/index.html', title="Welcome to CELTS!")
    except Exception as e:
        #TODO We have to return some sort of error page
        print('Error in main page:', e)
        return "",500
