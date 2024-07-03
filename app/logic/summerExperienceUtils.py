from app.models.summerExperience import SummerExperience

def saveSummerExperience(summer_experience_data):
    """
    Save the summer experience data to the database.
    
    Parameters:
    summer_experience_data (dict): Dictionary containing the summer experience data.
    """
    SummerExperience.create(**summer_experience_data)

