import json

from app.models import *

class EventTemplate(baseModel):
    name = CharField()
    tag = CharField()
    templateJSON = CharField()
    templateFile = CharField()
    isVisible = BooleanField(default=True)

    def fetch(self, key, default=None):
        """
            Get a key from the template data. Return the provided default value if the key is not found.
        """
        return self.templateData.get(key, default)

    @property
    def templateData(self):
        return json.loads(self.templateJSON)

    @templateData.setter
    def templateData(self, value):
        self.templateJSON = json.dumps(value)
