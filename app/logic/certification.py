from peewee import JOIN, fn, DoesNotExist, Case
from flask import g
from app.models.event import Event
from app.models.term import Term
from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement
from app.models.requirementMatch import RequirementMatch
from app.models.eventParticipant import EventParticipant
from app.models.user import User
import math
def termsAttended(certification, username):
    '''
    Retrieve terms attended by a user for certification and filter them based on frequency of a term
    '''
    attendedTerms = []
    attendance = (RequirementMatch.select()
                                    .join(EventParticipant, JOIN.LEFT_OUTER, on=(RequirementMatch.event == EventParticipant.event)) 
                                    .where(RequirementMatch.requirement_id == certification)  
                                    .where(EventParticipant.user == username))  
    for termRecord in range(len(attendance)):
        if not attendance[termRecord].event.term.isSummer:
            attendedTerms.append(attendance[termRecord].event.term.description)
    totalTerms = termsInTotal(username)
    attendedTerms = {term for term in attendedTerms if term in totalTerms}
    return attendedTerms
 

def termsInTotal(username):
    '''
    The function returns all non-summer academic terms a student should have, based on their class level where it finds
    the start term and populate from it with Fall-start alignment and special handling for NULL/Non-degree class level
    '''
    currentTerm = g.current_term
    currentDesc = currentTerm.description 
    if currentTerm.isSummer:
        currentDesc = f"Fall {currentTerm.year}"
    user = User.select().where(User.username == username).get()
    classLevel = ["Freshman", "Sophomore", "Junior", "Senior"]
    totalTerms = []
    for level, name in enumerate(classLevel):
        if user.rawClassLevel == name:
            totalTermsCount = (level + 1) * 2
            if currentDesc.startswith("Fall"):
                totalTermsCount -= 1  
            if currentDesc.startswith("Spring"):
                startYear = currentTerm.year - level - 1
            else:  
                startYear = currentTerm.year - level
            for k in range(totalTermsCount):
                if k % 2 == 0:  
                    season = "Fall"
                    year = startYear + (k // 2)
                else:           
                    season = "Spring"
                    year = startYear + (k // 2) + 1
                totalTerms.append(f"{season} {year}")
            break
   
    if user.rawClassLevel is None or user.rawClassLevel in ["NULL", "Graduating", "Non-Degree"]:
            totalTermsCount = 8 
            currentYear = currentTerm.year
            currentSeason = "Fall" if "Fall" in currentTerm.description else "Spring"
            for a in range(totalTermsCount):
                totalTerms.append(f"{currentSeason} {currentYear}")
                if currentSeason == "Fall":
                    currentSeason = "Spring"
                else: 
                    currentSeason = "Fall"
                    currentYear -= 1
            list.reverse(totalTerms) 
    return totalTerms

def termsMissed(certification, username): 
    '''
    Calculate how many certification-eligible terms a student has missed based on their class level
    and attendance record.
    '''
    totalTerms = termsInTotal(username) 
    attendedTerms = termsAttended(certification, username)
    missedTerms = [term for term in totalTerms if term not in attendedTerms]
    return missedTerms


def getCertRequirementsWithCompletion(*, certification, username):
    """
    Differentiate between simple requirements and requirements completion checking.
    """
    return getCertRequirements(certification, username, reqCheck=True)

def getCertRequirements(certification=None, username=None, reqCheck=False):
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
                .join(EventParticipant, JOIN.LEFT_OUTER, on=(RequirementMatch.event == EventParticipant.event) & (EventParticipant.user == username))
                .order_by(Certification.id, CertificationRequirement.order.asc(nulls="LAST")))
        # we have to add the is not null check so that `cert.requirement` always exists
        reqList = reqList.where(Certification.id == certification, CertificationRequirement.id.is_null(False))
        certificationList = []
        for cert in reqList:
            if username:
                cert.requirement.completed = bool(cert.__dict__['completed'])
                # this is to get the calculation when it comes to events with term, twice, annual as their frequency
                cert.requirement.attendedTerms = len(termsAttended(cert.requirement.id, username))
                cert.requirement.attendedDescriptions = termsAttended(cert.requirement.id, username)
                if cert.requirement.frequency == "term":
                    cert.requirement.missedTerms = len(termsMissed(cert.requirement.id, username))
                    cert.requirement.missedDescriptions = termsMissed(cert.requirement.id, username)
                    cert.requirement.totalTerms = len(termsInTotal(username))
                elif cert.requirement.frequency == "annual":
                    totalTerms = len(termsInTotal(username))
                    cert.requirement.attendedAnnual = len(termsAttended(cert.requirement.id, username))
                    cert.requirement.totalAnnual = int(math.floor(totalTerms/2+0.5)) if totalTerms % 2 == 1  else totalTerms/2
                elif cert.requirement.frequency == "once" and cert.requirement.completed:
                    term_record = (RequirementMatch
                            .select(RequirementMatch, Event, Term)
                            .join(Event)
                            .join(Term)
                            .where(RequirementMatch.requirement == cert.requirement.id)
                            .order_by(Term.year.desc())  # latest term first
                            .first()
                        )
                    cert.requirement.attendedTerm = term_record.event.term.description 
            certificationList.append(cert.requirement)

        # the .distinct() doesn't work efficiently, so we have to manually go through the list and removed duplicates that exist
        validCertification = set()
        certificationIndex = 0
        uniqueCertification = []
        
        for cert in certificationList:
            req = certificationList[certificationIndex]
            print(req.id, req.completed, "nyeet")
            if req not in validCertification:
                validCertification.add(req)
                uniqueCertification.append(req)
            # Override incomplete requirement when a completed 'once' requirement is found when removing duplicates
            elif reqCheck and req.frequency == "once" and req.completed: 
                for i in range(len(uniqueCertification)):
                    if uniqueCertification[i].id == req.id and not uniqueCertification[i].completed:
                        uniqueCertification[i] = req
                        validCertification.add(req)
            certificationIndex += 1
        certificationList = uniqueCertification
        print("Final List:", certificationList[0].id, certificationList[0].completed)
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
