from app.models import * 

def nameNumCombo(name, abbreviation):
        if name != '' and abbreviation != '':
            return f"{abbreviation} - {name}"
        elif name == '' and abbreviation == '':
            return " "
        elif name == '':
            return abbreviation
        elif abbreviation == '':
            return name

        