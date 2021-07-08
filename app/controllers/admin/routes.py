from flask import request, render_template
from flask import Flask, redirect, flash
from app.controllers.admin.createEvents import createEvent
from app.models.program import Program
from app.models.term import Term
from app.controllers.admin import admin_bp
from app.logic.adminCreateEvent import getAllFacilitators
from flask import g

@admin_bp.route('/testing_things', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"

@admin_bp.route('/<program>/create_event', methods=['GET'])
def createEventPage(program):
    listOfTerms = Term.select()
    facilitators = getAllFacilitators()
    user = g.current_user
    try:
        program = Program.get_by_id(program)

    except:
        return render_template(404)

    return render_template("admin/createEvents.html",
                            user = user,
                            program = program,
                            listOfTerms = listOfTerms,
                            facilitators = facilitators)
