from flask import abort, render_template, g, request
from app.controllers.admin import admin_bp

from app.models.term import Term

from app.logic.spreadsheet import create_spreadsheet

@admin_bp.route("/spreadsheetMaker")
def spreadsheetMaker():
    if not g.current_user.isCeltsAdmin:
        abort(403)
    
    academicYears = []
    allTerms = list(Term.select().order_by(Term.id))
    for term in allTerms:
        if term.academicYear not in academicYears:
            academicYears.append(term.academicYear)

    return render_template("/admin/spreadsheetMaker.html",
                           academicYears = academicYears)

@admin_bp.route("/createSpreadsheet/", methods=["POST"])
def createSpreadsheet():
    if not g.current_user.isCeltsAdmin:
        abort(403)

    formData = request.form
    print(formData.get("academicYear"))
    return ""