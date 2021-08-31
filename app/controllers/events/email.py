from flask import Flask, redirect, flash, url_for, request, g
from app.models.interest import Interest
from app.models.eventParticipant import EventParticipant
from app.controllers.events import events_bp





@events_bp.route('/email', methods=['POST'])
def emailVolunteers():

    emailInfo = request.form
    if emailInfo['emailRecipients'] == 'interested':    #email all students interested in the program
        volunteersToEmail = Interest.select().where(Interest.program == emailInfo['programID'])

    elif emailInfo['emailRecipients'] == 'eventParticipant':  #email only people who rsvped
        volunteersToEmail = EventParticipant.select().where(EventParticipant.event == emailInfo['eventID'])

    else:
        print("ITS IMPRESSIVE HOW YOU MANAGED TO BREAK THIS")

    print(list(volunteersToEmail))
    emails = [volunteer.user.email for volunteer in volunteersToEmail]
    print(emails)
    return redirect(url_for("events.events", term = 1))
