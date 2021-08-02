from flask import request, render_template, g, abort
from app.models.program import Program
from app.models.interest import Interest
from app.controllers.main import main_bp
from app.controllers.main.volunteerRegisterEvents import volunteerRegister

@main_bp.route('/')
def home():
    print(f"{g.current_user.username}: {g.current_user.firstName} {g.current_user.lastName}")
    try:
        return render_template('main/home.html', title="Welcome to CELTS!")
    except Exception as e:
        #TODO We have to return some sort of error page
        print('Error in main page:', e)
        return "",500

@main_bp.route('/volunteerIndicateInterest', methods = ['GET'])
def volunteerIndicateInterest():
    programs = Program.select()
    interests = Interest.select().where(Interest.user == g.current_user)
    interests_ids = [interest.program for interest in interests]
    return render_template('volunteerIndicateInterest.html',
                           title="Volunteer Interest",
                           user = g.current_user,
                           programs = programs,
                           interests = interests,
                           interests_ids = interests_ids)


@main_bp.route('/rsvpForEvent', methods = ['POST'])
def RSVPCaller():
    print("Hello")
    eventData = request.form.copy()
    volunteerRegister(eventData)

    return ""

@main_bp.route('/profile/<username>', methods = ['GET'])
def profilePage(username):

    if username == g.current_user.username or g.current_user.isCeltsAdmin or g.current_user.isCeltsStudentStaff:
        return f'<h1>Profile page for {username}</h1>'

    abort(403)
