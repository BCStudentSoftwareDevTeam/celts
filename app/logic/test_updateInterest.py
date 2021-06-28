from app.models.program import Program
from app.models.user import User
from app.models.interest import Interest
from app.controllers.main import main_bp


def updateInterest(program_id):
    """
    This function updates the interest table by adding a new row when a user
    shows interest in a program
    """
        rule = request.url_rule
        if 'addInterest' in rule.rule:
            Interest.get_or_create(program = program_id, user = g.current_user)
        else:
            deleted_interest = Interest.get(Interest.program == program_id and Interest.user == g.current_user)
            deleted_interest.delete_instance()
