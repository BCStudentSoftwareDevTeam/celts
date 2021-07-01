from flask import request, render_template
from flask import Flask, redirect, flash
from app.controllers.admin.createEvents import createEvents

from app.controllers.admin import admin_bp
from app.logic.adminCreateEvent import getTermDescription, getFacilitators, getCurrentTerm

@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/create_event', methods=['GET'])
def createEvent():
    termDescriptions = getTermDescription()
    eventFacilitator = getFacilitators()
    currentTerm = getCurrentTerm()
    return render_template("admin/createEvents.html",
                            listOfTermDescriptions = termDescriptions,
                            listOfEventFacilitators = eventFacilitator,
                            theCurrentTerm = currentTerm )


@admin_bp.route('/create_event1', methods=['GET'])
def createEvent1():
    termDescriptions = getTermDescription()
    eventFacilitator = getFacilitators()
    currentTerm = getCurrentTerm()
    return render_template("admin/testing.html",
                            listOfTermDescriptions = termDescriptions,
                            listOfEventFacilitators = eventFacilitator,
                            theCurrentTerm = currentTerm )
