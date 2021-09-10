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
        volunteersToEmail = User.select().where(User.username == 'neillz')
        # THIS WORKS
    else:
        print("ITS IMPRESSIVE HOW YOU MANAGED TO BREAK THIS")

    mail = emailHandler(emailInfo)
    emails = [user.email for user in volunteersToEmail]
    mail.sendEmail(Message(emailInfo['subject'], emails, emailInfo['message']), emails)
    # with mail.mail.connect() as conn:    <--- this doesn't actually use the class
    #     if 'sendIndividually' in emailInfo:
    #         for user in volunteersToEmail:
    #             # print(user)
    #             conn.sendEmail(Message(emailInfo['subject'], [user.email], emailInfo['message']))
    #     else:
    #         emails = [user.email for user in volunteersToEmail]
    #         conn.sendEmail(Message(emailInfo['subject'], emails, emailInfo['message']))
        # conn.send(Message(emailInfo['subject'], [user.email , "j5u6j9w6v1h0p3g1@bereacs.slack.com"], emailInfo['message']))
        # password for bramsayr@gmail.com is celtsTest
    flash("Email successfully sent!", "success")
    return redirect(url_for("events.events", term = 1))
