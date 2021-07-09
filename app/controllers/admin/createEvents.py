import datetime
from app.models.event import Event
from app.models.term import Term
from flask import json, jsonify
from flask import request
from app.controllers.admin import admin_bp
from app.logic.adminCreateEvent import getTermDescription
from app.logic.adminNewEvent import createEvent, manageNewEventData, eventEdit
from app.logic.validateNewEvent import validateNewEventData
from app.models.facilitator import Facilitator
from flask import flash, redirect, url_for, g

@admin_bp.route('/createEvents', methods=['POST'])
@admin_bp.route('/eventEdit', methods=['POST'])
def createEvents():

    if g.current_user.isCeltsAdmin:
        #add check for admin
        EventData = request.form.copy() #since request.form returns a immutable dict. we need to copy to change the
        newEventData= manageNewEventData(EventData)
        eventId = newEventData['eventId']

        # add function to validate data ()
        validNewEventData, eventErrorMessage = validateNewEventData(newEventData)

        if validNewEventData:
            if not eventId:
                createEvent(newEventData)

                flash("Event successfully created!")
                return redirect(url_for("admin.createEvent", program_id=newEventData['programId']))

            else:
                eventEdit(newEventData)
                flash("Event successfully Updated!")
                return redirect(url_for("admin.createEvent", program_id=newEventData['programId']))
        else:
            flash(eventErrorMessage)
            return redirect(url_for("admin.createEvent", program_id=2)) #FIXME: have this redirect to main programs page (or some appropriate non admin page).

    flash("Only celts admins can create an event!")
    return redirect(url_for("admin.createEvent", program_id=2)) #FIXME: have this redirect to main programs page (or some appropriate non admin page).
