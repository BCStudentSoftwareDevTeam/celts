from app.models import * 

def displayName(name, abbreviation):
        '''
        This function combines course name and numbers with conditions
        inputs: course name, course abbreviation
        '''
        if name and abbreviation:
            return f"{abbreviation} - {name}"
        elif not name and not abbreviation:
            return ''
        elif not name:
            return abbreviation
        elif not abbreviation:
            return name

        