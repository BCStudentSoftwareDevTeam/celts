from flask import request, render_template, redirect, url_for, flash, abort, g, json, jsonify, session
from peewee import DoesNotExist, JOIN
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from app.controllers.admin import admin_bp
from app.models.event import Event
from app.models.program import Program
from app.models.user import User
from app.models.eventParticipant import EventParticipant
from app.models.emergencyContact import EmergencyContact
from app.logic.searchUsers import searchUsers
from app.logic.volunteers import updateEventParticipants, getEventLengthInHours, addUserBackgroundCheck, setProgramManager, deleteUserBackgroundCheck
from app.logic.participants import trainedParticipants, addPersonToEvent, getParticipationStatusForTrainings, sortParticipantsByStatus
from app.logic.events import getPreviousSeriesEventData, getEventRsvpCount
from app.models.eventRsvp import EventRsvp
from app.models.backgroundCheck import BackgroundCheck
from app.logic.createLogs import createActivityLog, createRsvpLog
from app.logic.users import getBannedUsers, isBannedFromEvent

@admin_bp.route('/event/<eventID>/manage_labor', methods=['GET', 'POST'])
def getlabor(eventID):
    '''Accepts user input and queries the database returning results that matches user search'''
    name = "hi world"
    return name