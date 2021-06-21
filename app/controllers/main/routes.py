from flask import request, render_template, g

from app.controllers.main import main_bp

@main_bp.route('/')
def home():
    print(f"{g.current_user.username}: {g.current_user.firstName} {g.current_user.lastName}")
    return render_template('home.html', title="Welcome to CELTS!") 
