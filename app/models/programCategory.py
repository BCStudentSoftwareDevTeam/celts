from app.models import*

class ProgramCategory(baseModel):
    categoryName = CharField(primary_key=True)
