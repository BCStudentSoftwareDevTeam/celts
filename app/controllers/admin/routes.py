from flask import request, render_template
from flask import Flask, redirect, flash
from app.controllers.admin.createEvents import createEvent
from app.models.program import Program
from app.controllers.admin import admin_bp
from flask import g, url_for
from app.models.term import Term
from app.logic.getAllFacilitators import getAllFacilitators
from app.logic.programSelect import eventElements


@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/create_event', methods=['POST'])
def createEventPage():
    programSelect = request.form.copy()
    programChoice = programSelect.get("programChoice")
    createEventsDict = {}
    createEventsDict = {"program": programChoice}
    eventElementsDict = eventElements()
    listOfTerms = Term.select()
    facilitators = getAllFacilitators()


    return render_template("admin/createEvents.html",
                            program = programChoice,
                            listOfTerms = listOfTerms,
                            facilitators = facilitators,
                            )

@admin_bp.route('/program_select', methods=['GET'])
def programSelect():

    getPrograms = Program.select()

    return render_template("admin/programSelect.html",
                            getPrograms = getPrograms,)
