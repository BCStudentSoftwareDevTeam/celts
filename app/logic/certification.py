from peewee import JOIN, DoesNotExist

from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement
from app.models.requirementMatch import RequirementMatch

def getCertRequirements(certification=None):
    """
    Return the requirements for all certifications, or for one if requested.

    Keyword arguments:
        certification -- The id or object for a certification to request

    Returns:
        A list of dictionaries with all certification data and requirements. If `certification`
        is given, returns only a list of requirement objects for the given certification.
    """
    reqList = (Certification.select(Certification, CertificationRequirement)
                         .join(CertificationRequirement, JOIN.LEFT_OUTER, attr="requirement")
                         .order_by(Certification.id, CertificationRequirement.order.asc(nulls="LAST")))
    if certification:
        # we have to add the is not null check so that `cert.requirement` always exists
        reqList = reqList.where(Certification.id == certification, CertificationRequirement.id.is_null(False))
        return [cert.requirement for cert in reqList]
    
    certs = {}
    for cert in reqList:
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
    saveIds = [requirementData['id'] for requirementData in newRequirements]
    CertificationRequirement.delete().where(CertificationRequirement.id.not_in(saveIds)).execute()


    # update existing and add new requirements
    requirements = []
    for order, requirementData in enumerate(newRequirements):
        try:
            newRequirement = CertificationRequirement.get_by_id(requirementData['id'])
        except DoesNotExist:
            newRequirement = CertificationRequirement()

        newRequirement.certification = certId
        newRequirement.isRequired = bool(requirementData['required'])
        newRequirement.frequency = requirementData['frequency']
        newRequirement.name = requirementData['name']
        newRequirement.order = order
        newRequirement.save()

        requirements.append(newRequirement)

    return requirements 

def updateCertRequirementForEvent(event, requirement):
    """
    Add a certification requirement to an event. 
    Replaces the requirement for an event if the event already exists.

    Arguments:
        event - an Event object or id
        requirement - a CertificationRequirement object or id
    """
    # delete existing matches for our event
    for match in RequirementMatch.select().where(RequirementMatch.event == event):
        match.delete_instance()

    RequirementMatch.create(event=event, requirement=requirement)
