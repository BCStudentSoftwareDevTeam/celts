from app.models import*
from app.models.term import Term


def getTermDescription():

    termDescription = Term.select(Term.description)

    description = [des.description for des in termDescription.objects()]

    return description
