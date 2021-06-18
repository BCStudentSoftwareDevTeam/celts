from flask import request, render_template, g

from app.controllers.main import main_bp

@main_bp.route('/')
def home():
    print(f"{g.current_user.username}: {g.current_user.firstName} {g.current_user.lastName}")
    try:
        return render_template('main/home.html', title="Welcome to CELTS!")
    except Exception as e:
        #TODO We have to return some sort of error page
        print('Error in main page:', e)
        return "",500
