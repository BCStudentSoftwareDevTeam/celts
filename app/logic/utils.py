import collections
from peewee import DoesNotExist
from app.models.term import Term
from datetime import datetime

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
                            .where((Term.year <= currentTerm.year + 2)))

    return surroundingTerms

def deep_update(d, u):
    """
    Update old_dict in place with the values from new_dict, respecting nested dictionaries.
    Adapted from this stackoverflow answer: https://stackoverflow.com/a/32357112
    """
    if d is None: d = {}
    if not u: return d

    for key, val in u.items():
        if isinstance(d, collections.Mapping):
            if isinstance(val, collections.Mapping):
                r = deep_update(d.get(key, {}), val)
                d[key] = r
            else:
                d[key] = u[key]
        else:
            d = {key: u[key]}

    return d

def getStartofCurrentAcademicYear(currentTerm):
    if ("Summer" in currentTerm.description) or ("Spring" in currentTerm.description):
        fallTerm = Term.select().where(Term.year==currentTerm.year-1, Term.description == f"Fall {currentTerm.year-1}").get()
        return fallTerm
    return currentTerm

def format24HourTime(timeStr):
    """

    timeStr: expects a string HH:mm
    """
    print("----", type(timeStr))
    timeThing = format24to12HourTime(timeStr)

    # try:
    # if type(time_str) is str:
    time = datetime.strptime(timeThing, "%I:%M %p").strftime("%H:%M") # Converts string to datetime and formats correctly
    print("====", time)
    print("====", type(time))
    # except Exception as e:
    # # else:
    #     print("----", e)
    #     time_str.strftime("%H:%M")

    return time

def format24to12HourTime(timeStr):
    """
    """
    if int(timeStr[:2]) > 12:
        formattedTime = "0" + str(int(timeStr[:2]) - 12) + timeStr[2:] + " PM"
    elif int(timeStr[:2]) < 12:
        formattedTime =  timeStr + " AM"
    else:
        formattedTime = timeStr + " PM"
    return formattedTime
