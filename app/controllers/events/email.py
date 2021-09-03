from flask import Flask, redirect, flash, url_for, request, g
from app.models.interest import Interest
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.controllers.events import events_bp

@events_bp.route('/email', methods=['POST'])
def emailVolunteers():

    emailInfo = request.form
    if emailInfo['emailRecipients'] == 'interested':    #email all students interested in the program
        volunteersToEmail = User.select().join(Interest).where(Interest.program == emailInfo['programID'])

    elif emailInfo['emailRecipients'] == 'eventParticipant':  #email only people who rsvped
        volunteersToEmail = User.select().join(EventParticipant).where(EventParticipant.event == emailInfo['eventID'])

    elif emailInfo['emailRecipients'] == 'yourself':  #email yourself; test purposes maybe
        volunteersToEmail = User.select().where(User.username == g.current_user.username)

    else:
        print("ITS IMPRESSIVE HOW YOU MANAGED TO BREAK THIS")
        # I found a way :(
        
    emails = [volunteer.email for volunteer in volunteersToEmail]
    print(f'Volunteers to email: {emails}')

    return redirect(url_for("events.events", term = 1))
