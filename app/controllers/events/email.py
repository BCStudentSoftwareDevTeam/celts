from flask import Flask, redirect, flash, url_for, request, g
from flask_mail import Mail, Message
from app.models.interest import Interest
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.logic.emailHandler import *
from app.controllers.events import events_bp
from app import app

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

    #testing the things in emailHandler file
    default_cfg = load_config('app/config/default.yml') #this works yay
    print(default_cfg['mail'])
    #mail = emailHandler(emailInfo)
    mail = Mail(app)
    #check mail_test.py in lsf to see what the following is trying to do
    msg = Message(emailInfo['message'], recipients=['j5u6j9w6v1h0p3g1@bereacs.slack.com'], sender="support@bereacollege.onmicrosoft.com")

    mail.send(msg)
    

    return redirect(url_for("events.events", term = 1))
