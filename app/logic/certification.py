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
    """
    # check for missing ids to remove
    newIds = [req['id'] for req in newRequirements]
    missingReqs = CertificationRequirement.select().where(CertificationRequirement.id.not_in(newIds))
    for req in missingReqs:
        req.delete_instance()


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
