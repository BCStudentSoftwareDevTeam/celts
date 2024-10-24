from flask import g, render_template, request, abort, flash, redirect, url_for, jsonify
from peewee import DoesNotExist

from app.controllers.minor import minor_bp
from app.models.user import User
from app.models.term import Term
from app.models.summerExperience import SummerExperience
from app.models.otherExperience import OtherExperience

from app.logic.fileHandler import FileHandler
from app.logic.utils import selectSurroundingTerms, getFilesFromRequest
from app.logic.minor import getProgramEngagementHistory, getCourseInformation, getCommunityEngagementByTerm, removeSummerExperience
from app.logic.minor import saveOtherEngagementRequest, setCommunityEngagementForUser, saveSummerExperience, getSummerTerms, getSummerExperience, getEngagementTotal, createSummerExperience, createOtherEngagement
import logging


# ################################################## SUMMER EXPERIENCE START ###########################################################

@minor_bp.route('/cceMinor/<username>/addSummerExperience', methods=['POST'])
def addASummerExperience(username):
    try:
        createSummerExperience(username, request.form)
        flash(f'Summer Experience added successfully by {username}', 'success')
        return redirect(url_for('minor.viewProposal', username=username, activeTab='trainingEvents'))
    except Exception as e:
        flash(f'An error occurred while adding the summer experience: {e}', 'danger')
        logging.error(f'An error occurred while adding the summer experience: {e}')
    return redirect(url_for('minor.viewCceMinor', username=username))



@minor_bp.route('/cceMinor/<username>/viewProposal', methods=['GET'])
def viewProposal(username):
    try:
        user = User.get(User.username == username)
        try:
            summer_experience = (SummerExperience
                                 .select()
                                 .where(SummerExperience.user == user)
                                 .order_by(SummerExperience.id.desc())
                                 .get())
        except SummerExperience.DoesNotExist:
            summer_experience = None  # No summer experience found

        return render_template('minor/profile.html', user=user, summer_experience=summer_experience, activeTab='trainingEvents')
   
    except Exception as e:
        flash(f"Error retrieving proposal: {e}", 'danger')
        return redirect(url_for('minor.viewCceMinor', username=username))




@minor_bp.route('/profile/<username>/withdrawSummerExperience', methods=['POST'])
def withdrawSummerExperience(username):
    try:
        user = User.get(User.username == username)
        experience_id = request.form.get('experience_id')
        
        summer_experience = SummerExperience.get(SummerExperience.id == experience_id, SummerExperience.user == user)
        summer_experience.delete_instance()
        
        flash('Summer experience proposal withdrawn successfully.', 'success')
        return jsonify({'status': 'success', 'message': 'Summer experience proposal withdrawn successfully.'})
    except Exception as e:
        logging.error(f"Error withdrawing summer experience: {e}")
        flash('An error occurred while withdrawing the proposal.', 'danger')
        return jsonify({'status': 'error', 'message': 'An error occurred while withdrawing the proposal.'}), 500




@minor_bp.route('/cceMinor/<username>/updateSummerExperience', methods=['GET', 'POST'])
def updateSummerExperience(username):
    try:
        form_data = request.form
        user = User.get(User.username == username)
        experience_id = form_data['experience_id']
        summer_experience = SummerExperience.get(SummerExperience.id == experience_id)

        content_area = ', '.join(form_data.getlist('contentArea'))
        experience_type = form_data['experienceType']
        if experience_type == 'Other':
            other_experience_description = form_data.get('otherExperienceDescription', '')
            if not other_experience_description:
                raise ValueError("Other experience description is required.")
            experience_type = other_experience_description

        summer_experience.studentName = form_data['studentName']
        summer_experience.summerYear = form_data['summerYear']
        summer_experience.roleDescription = form_data['roleDescription']
        summer_experience.experienceType = experience_type
        summer_experience.CceMinorContentArea = content_area
        summer_experience.experienceHoursOver300 = form_data['experienceHoursOver300'] == 'Yes'
        summer_experience.experienceHoursBelow300 = form_data.get('experienceHoursBelow300')
        summer_experience.company = form_data['company']
        summer_experience.companyAddress = form_data['companyAddress']
        summer_experience.companyPhone = form_data['companyPhone']
        summer_experience.companyWebsite = form_data['companyWebsite']
        summer_experience.supervisorName = form_data['directSupervisor']
        summer_experience.supervisorPhone = form_data['supervisorPhone']
        summer_experience.supervisorEmail = form_data['supervisorEmail']
        summer_experience.save()

        flash("Proposal updated successfully.", 'success')
        return redirect(url_for('minor.viewProposal', username=username))
    except Exception as e:
        flash(f"Error updating proposal: {e}", 'danger')
        return redirect(url_for('minor.viewProposal', username=username))


# ################################################## SUMMER EXPERIENCE END ###########################################################
@minor_bp.route('/cceMinor/<username>/addOtherEngagement', methods=['POST'])
def addOtherEngagement(username):
    try:
        form_data = request.form
        # Process form data and create a new OtherExperience
        new_experience = OtherExperience.create(
            user=User.get(User.username == username),
            activity=form_data['experienceName'],
            term=Term.get(Term.id == form_data['term']),
            hours=form_data['totalHours'],
            weeks=form_data['weeks'],
            service=form_data['description'],
            company=form_data['companyOrOrg']
            # Add other fields as needed
        )
        flash('Other Community Engaged Experience added successfully!', 'success')
        return redirect(url_for('minor.view_other_engagement', username=username))
    except Exception as e:
        flash(f'An error occurred while adding the engagement: {e}', 'danger')
        logging.error(f'An error occurred while adding the engagement: {e}', exc_info=True)
        return redirect(url_for('minor.view_other_engagement', username=username))

@minor_bp.route('/cceMinor/<username>/otherEngagement', methods=['GET'])
def view_other_engagement(username):
    user = User.get(User.username == username)
    try:
        other_experience = OtherExperience.get(OtherExperience.user == user)
    except OtherExperience.DoesNotExist:
        other_experience = None
    return render_template('minor/profile.html', user=user, other_experience=other_experience)




@minor_bp.route('/api/terms', methods=['GET'])
def get_terms():
    terms = Term.select()
    term_list = [{'id': term.id, 'name': term.description} for term in terms]
    return jsonify(term_list)


@minor_bp.route('/withdrawOtherExperience/<int:experience_id>', methods=['POST'])
def withdraw_other_experience(experience_id):
    try:
        experience = OtherExperience.get(OtherExperience.id == experience_id)
        experience.delete_instance()
        return jsonify({'status': 'success', 'message': 'Experience withdrawn successfully.'})
    except Exception as e:
        logging.error(f"Error withdrawing other experience: {e}", exc_info=True)
        return jsonify({'success': False, 'An error occured while withrawing experience.': str(e)}), 500

@minor_bp.route('/cceMinor/<username>/editOtherEngagement', methods=['POST'])
def edit_other_engagement(username):
    try:
        form_data = request.form
        experience_id = form_data['experience-id']
        experience = OtherExperience.get(OtherExperience.id == experience_id)
        
        experience.activity = form_data['experienceName']
        experience.term = Term.get(Term.id == form_data['term'])
        experience.hours = form_data['totalHours']
        experience.weeks = form_data['weeks']
        experience.service = form_data['description']
        experience.company = form_data['companyOrOrg']
        experience.save()
        
        flash(f'Engagement updated successfully by {username}', 'success')
    except Exception as e:
        flash(f'An error occurred while updating the engagement: {e}', 'danger')
        logging.error(f'An error occurred while updating the engagement: {e}', exc_info=True)
    return redirect(url_for('minor.viewCceMinor', username=username))

# ###############################################################################

@minor_bp.route('/profile/<username>/cceMinor', methods=['GET'])
def viewCceMinor(username):
    """
        Load minor management page with community engagements and summer experience
    """
    if not (g.current_user.isAdmin):
        return abort(403)

    sustainedEngagementByTerm = getCommunityEngagementByTerm(username)
    selectedSummerTerm, summerExperience = getSummerExperience(username)

    return render_template("minor/profile.html",
                            user = User.get_by_id(username),
                            sustainedEngagementByTerm = sustainedEngagementByTerm,
                            summerExperience = summerExperience if summerExperience else "",
                            selectedSummerTerm = selectedSummerTerm,
                            totalSustainedEngagements = getEngagementTotal(sustainedEngagementByTerm),
                            summerTerms = getSummerTerms(),
                            allTerms = getSummerExperience(username))

    

@minor_bp.route('/cceMinor/<username>/getEngagementInformation/<type>/<term>/<id>', methods=['GET'])
def getEngagementInformation(username, type, id, term):
    """
        For a particular engagement activity (program or course), get the participation history or course information respectively.
    """
    if type == "program":
        information = getProgramEngagementHistory(id, username, term)
    else:
        information = getCourseInformation(id)

    return information

@minor_bp.route('/cceMinor/<username>/modifyCommunityEngagement', methods=['PUT','DELETE'])
def modifyCommunityEngagement(username):
    """
        Saving a term participation/activities for sustained community engagement
    """
    if not g.current_user.isCeltsAdmin:
        abort(403)

    action = 'add' if request.method == 'PUT' else 'remove'
    try: 
        setCommunityEngagementForUser(action, request.form, g.current_user)
    except DoesNotExist:
        return "There are already 4 Sustained Community Engagement records." 
    
    return ""

@minor_bp.route('/cceMinor/<username>/requestOtherCommunityEngagement', methods=['GET', 'POST'])
def requestOtherEngagement(username):
    """
        Load the "request other" form and submit it.
    """
    user = User.get_by_id(username)
    terms = selectSurroundingTerms(g.current_term)
    

    if request.method == 'POST':
        filename = None
        attachment = request.files.get("attachmentObject")
        if attachment:
                addFile = FileHandler(getFilesFromRequest(request))
                addFile.saveFiles()
                filename = attachment.filename
        formData = request.form.copy()
        formData["filename"] = filename
        saveOtherEngagementRequest(formData)
        flash("Other community engagement request submitted.", "success")
        return redirect(url_for("minor.viewCceMinor", username=user))


    return render_template("/minor/requestOtherEngagement.html",
                            user=user,
                            terms=terms)

# @minor_bp.route('/cceMinor/<username>/addSummerExperience', methods=['POST'])
def addSummerExperience(username):
    saveSummerExperience(username, request.form, g.current_user)

    return ""

@minor_bp.route('/cceMinor/<username>/deleteSummerExperience', methods=['POST'])
def deleteSummerExperience(username):        
    removeSummerExperience(username)

    return ""