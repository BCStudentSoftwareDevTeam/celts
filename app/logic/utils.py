from datetime import datetime
import collections.abc as collections

from flask import session
from peewee import DoesNotExist

from app.models.term import Term

def selectSurroundingTerms(currentTerm, prevTerms=2):
    """
    Returns a list of term objects around the provided Term object for the current term.
    Chooses the previous terms according to the prevTerms parameter (defaulting to 2),
    and then chooses terms for the next two years after the current term.

    To get only the current and future terms, pass prevTerms=0.
    """
    startTerm = max(1, currentTerm.id - prevTerms)
    surroundingTerms = (Term.select()
                            .where(Term.id >= startTerm)
                            .where((Term.year <= currentTerm.year + 2))
                            .order_by(Term.termOrder))

    return surroundingTerms

def getStartofCurrentAcademicYear(currentTerm):
    if ("Summer" in currentTerm.description) or ("Spring" in currentTerm.description):
        fallTerm = Term.select().where(Term.year==currentTerm.year-1, Term.description == f"Fall {currentTerm.year-1}").get()
        return fallTerm
    return currentTerm

def format24HourTime(unformattedTime):
    """
    Turns a time string or datetime object into a string with a time in 24 hour format
    unformattedTime: expects a string with format HH:mm AM/PM or HH:mm OR a datetime object
    returns: a string in 24 hour format HH:mm
    """
    if type(unformattedTime) == str:
        try:
            formattedTime = datetime.strptime(unformattedTime, "%I:%M %p").strftime("%H:%M") # Converts string to datetime then back to string and formats correctly
            return formattedTime
        except ValueError:
            #  calling strptime here to explicitly raise an exception if it wasn't properly in 24 hour format
            formattedTime = datetime.strptime(unformattedTime, "%H:%M")
            return unformattedTime
    else:
        formattedTime = unformattedTime.strftime("%H:%M")
        return formattedTime

def getUsernameFromEmail(email):
    return email.split("@")[0]

def getFilesFromRequest(request):
    attachmentFiles = request.files.getlist("attachmentObject")
    fileDoesNotExist = attachmentFiles[0].content_type == "application/octet-stream"
    if fileDoesNotExist:
        attachmentFiles = None

    return attachmentFiles

def getRedirectTarget(popTarget=False):
    """
    This function returns a string with the URL or route to a page in the Application
        saved with setRedirectTarget() and is able to pop the value from the session
        to make it an empty value
    popTarget: expects a bool value to determine whether or not to reset
                redirectTarget to an emtpy value
    return: a string with the URL or route to a page in the application that was
            saved in setRedirectTarget()
    """
    if "redirectTarget" not in session:
        return ''

    target = session["redirectTarget"]
    if popTarget:
        session.pop("redirectTarget")
    return target

def setRedirectTarget(target):
    """
    This function saves the target URL in the session for future redirection
        to said page
    target: expects a string that is a URL or a route to a page in the application
    return: None
    """
    session["redirectTarget"] = target

