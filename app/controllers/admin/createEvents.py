import datetime
from app.models.event import Event
from app.models.term import Term
from flask import json, jsonify
from flask import request
from app.controllers.admin import admin_bp
from app.logic.adminNewEvent import createNewEvent, setValueForUncheckedBox
from app.logic.validateNewEvent import validateNewEventData
from app.models.facilitator import Facilitator
from flask import flash, redirect, url_for, g

@admin_bp.route('/createEvent', methods=['POST'])
def createEvent():

    if g.current_user.isCeltsAdmin:
        #add check for admin
        eventData = request.form.copy() #since request.form returns a immutable dict. we need to copy to change the
        newEventData= setValueForUncheckedBox(eventData)

        # add function to validate data ()
        validNewEventData, eventErrorMessage = validateNewEventData(newEventData)

        if validNewEventData:
            createNewEvent(newEventData)

            flash("Event successfully created!")
            return redirect(url_for("admin.createEventPage", program_id=newEventData['programId']))

        else:
            flash(eventErrorMessage)
            return redirect(url_for("admin.createEventPage", program_id=2)) #FIXME: have this redirect to main programs page (or some appropriate non admin page).

    flash("Only celts admins can create an event!")
    return redirect(url_for("admin.createEventPage", program_id=2)) #FIXME: have this redirect to main programs page (or some appropriate non admin page).
