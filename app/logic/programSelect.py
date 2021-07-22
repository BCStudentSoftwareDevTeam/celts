from app.models.term import Term
from app.controllers.admin import admin_bp
from app.logic.getAllFacilitators import getAllFacilitators
from flask import flash, redirect, url_for, g

def eventElements():
    listOfTerms = Term.select()
    facilitators = getAllFacilitators()
    eventElementsDict = {"term": listOfTerms, "facilitators": facilitators}

    return eventElementsDict
