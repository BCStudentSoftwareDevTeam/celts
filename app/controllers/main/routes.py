from flask import request, render_template

from app.controllers.main import main_bp

@main_bp.route('/')
def home():
   return render_template('home.html', title="Welcome to CELTS!") 
