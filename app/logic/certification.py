from peewee import JOIN, DoesNotExist, Case
from flask import g
from app.models.event import Event
from app.models.term import Term
from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement
from app.models.requirementMatch import RequirementMatch
from app.models.eventParticipant import EventParticipant
from app.models.user import User

def termsAttended(certification=None, username=None):
    '''
    Retrieve terms attended by a user for certification and filter them based on frequency of a term
    '''
    attendedTerms = []
    if username:
        attendance = (RequirementMatch.select()
                                      .join(EventParticipant, JOIN.LEFT_OUTER, on=(RequirementMatch.event == EventParticipant.event)) 
                                      .where(RequirementMatch.requirement_id == certification)  
                                      .where(EventParticipant.user == username))  
    for termRecord in range(len(attendance)):
        attendedTerms.append(attendance[termRecord].event.term.description)
    return attendedTerms
            
def termsMissed(certification=None, username=None): 
    '''
    Calculate how many certification-eligible terms a student has missed based on their class level
    and attendance record.

    Logic:
    - Each class level is expected to participate in 2 terms per year.
    - If the user is currently in their final spring term (e.g., Spring of senior year), 
      they are expected to have completed all terms: missedTerms = (level + 1) * 2.
    - Otherwise, assume they’ve had one fewer term to attend: missedTerms = ((level + 1) * 2) - 1.
    - If the user's classification is None, assume just 1 expected term.
    - Subtract the number of terms the student has attended from the expected total to get the missed count.
    '''
    classLevel = ["Freshman", "Sophomore", "Junior", "Senior"]
    currentTerm = g.current_term 
    currentDescription = currentTerm.description
    
    # looking into a scenario where the current term is summer so that we can reassigned the current term variable to the next term     
    if currentTerm.isSummer == True:
        currentDescription = f'Fall {currentTerm.year}'
        currentTerm = Term.select(Term).where(Term.description == currentDescription).get()
    else:
        currentDescription = currentTerm.description

    for level in range(4):
        user = User.select().where(User.username == username).get()
        if user.rawClassLevel == classLevel[level] and currentDescription == f'Spring {currentTerm.year}':
            missedTerms = (level + 1) * 2
        elif user.rawClassLevel == classLevel[level]:
            missedTerms = ((level + 1) * 2) - 1
        elif str(user.rawClassLevel) == "None":
            missedTerms = 1
            
    attendedTerms = termsAttended(certification, username)
    missedTerms = missedTerms - len(attendedTerms)
    
    return missedTerms

def getCertRequirementsWithCompletion(*, certification, username):
    """
    Differentiate between simple requirements and requirements completion checking.
    """
    return getCertRequirements(certification, username)

def getCertRequirements(certification=None, username=None):
    """
    Return the requirements for all certifications, or for one if requested.

    Keyword arguments:
        certification -- The id or object for a certification to request
        username -- The username to check for completion

    Returns:
        A list of dictionaries with all certification data and requirements. If `certification`
        is given, returns only a list of requirement objects for the given certification. If 
        `username` is given, the requirement objects have a `completed` attribute.
    """
    reqList = (Certification.select(Certification, CertificationRequirement)
                            .join(CertificationRequirement, JOIN.LEFT_OUTER, attr="requirement")
                            .order_by(Certification.id, CertificationRequirement.order.asc(nulls="LAST")))
    if certification:
        if username:
            # I don't know how to add something to a select, so we have to recreate the whole query :(
            completedCase = Case(None, ((EventParticipant.user_id.is_null(True), 0),), 1)
            reqList = (Certification
                .select(Certification, CertificationRequirement, completedCase.alias("completed"))
                .join(CertificationRequirement, JOIN.LEFT_OUTER, attr="requirement")
                .join(RequirementMatch, JOIN.LEFT_OUTER)
                .join(EventParticipant, JOIN.LEFT_OUTER, on=(RequirementMatch.event == EventParticipant.event))
                .where(EventParticipant.user.is_null(True) | (EventParticipant.user == username))
                .order_by(Certification.id, CertificationRequirement.order.asc(nulls="LAST")))

        # we have to add the is not null check so that `cert.requirement` always exists
        reqList = reqList.where(Certification.id == certification, CertificationRequirement.id.is_null(False))
        certificationList = []
        for cert in reqList:
            if username:
                cert.requirement.completed = bool(cert.__dict__['completed'])
                # this is to get the calculation when it comes to events with term as their frequency
                if cert.requirement.frequency == "term":
                    cert.requirement.missedTerms = termsMissed(cert.requirement.id, username)
                    cert.requirement.attendedTerms = len(termsAttended(cert.requirement.id, username))
                    cert.requirement.attendedDescriptions = termsAttended(cert.requirement.id, username)
            certificationList.append(cert.requirement)

        # the .distinct() doesn't work efficiently, so we have to manually go through the list and removed duplicates that exist
        validCertification = set()
        certificationIndex = 0
        
        for cert in certificationList:
            if certificationList[certificationIndex] not in validCertification:
                validCertification.add(certificationList[certificationIndex])
            certificationIndex += 1
            
        certificationList = list(validCertification)
        
        return certificationList
    
    certificationDict = {}
    for cert in reqList:
        if cert.id not in certificationDict.keys():
            certificationDict[cert.id] = {"data": cert, "requirements": []}
        if getattr(cert, 'requirement', None):
            certificationDict[cert.id]["requirements"].append(cert.requirement)
            
    return certificationDict

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
    CertificationRequirement.delete().where(CertificationRequirement.certification_id == certId, CertificationRequirement.id.not_in(saveIds)).execute()

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
