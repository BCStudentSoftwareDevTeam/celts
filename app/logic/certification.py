from peewee import JOIN, DoesNotExist

from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement

def getCertRequirements(certification=None):
    """
    Return the requirements for all certifications, or for one if requested.

    Keyword arguments:
        certification -- The id or object for a certification to request

    Returns:
        A list of dictionaries with all certification data and requirements. If `certification`
        is given, returns only a list of requirement objects for the given certification.
    """
    query = (Certification.select(Certification, CertificationRequirement)
                         .join(CertificationRequirement, JOIN.LEFT_OUTER, attr="requirement")
                         .order_by(Certification.id, CertificationRequirement.order.asc(nulls="LAST")))
    if certification:
        # we have to add the is not null check so that `cert.requirement` always exists
        query = query.where(Certification.id == certification, CertificationRequirement.id.is_null(False))
        return [cert.requirement for cert in query]
    
    certs = {}
    for cert in query:
        if cert.id not in certs.keys():
            certs[cert.id] = {"data": cert, "requirements": []}

        if getattr(cert, 'requirement', None):
            certs[cert.id]["requirements"].append(cert.requirement)

    return certs

def updateCertRequirements(certId, newRequirements):
    """
    Update the certification requirements in the database to match the provided list of requirement data.

    The order of the list matters. Any ids that are in the database and not in `newRequirements` will be 
    removed. IDs that do not exist in the database will be created (and given a new, auto-generated ID).

    Arguments:
        certId - The id of the certification whose requirements we are updating
        newRequirements - a list of dictionaries. Each dictionary needs 'id', 'required', 'frequency', and 'name'.

    Returns:
        A list of CertificationRequirement objects corresponding to the given `newRequirements` list.
    """
    # check for missing ids to remove
    newIds = [req['id'] for req in newRequirements]
    CertificationRequirement.delete().where(CertificationRequirement.id.not_in(newIds)).execute()


    # update existing and add new requirements
    requirements = []
    for order,req in enumerate(newRequirements):
        try:
            newreq = CertificationRequirement.get_by_id(req['id'])
        except DoesNotExist:
            newreq = CertificationRequirement()

        newreq.certification = certId
        newreq.isRequired = bool(req['required'])
        newreq.frequency = req['frequency']
        newreq.name = req['name']
        newreq.order = order
        newreq.save()

        requirements.append(newreq)

    return requirements 
