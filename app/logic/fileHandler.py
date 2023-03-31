import os
from flask import redirect, url_for
from app import app
from app.models.eventFile import EventFile

class FileHandler:
    def __init__(self,files=None):
        self.files=files
        self.path= app.config['files']['event_attachment_path']

    def getFileFullPath(self, eventId=None, newfile = None):
        """
        This creates the directory/path for the object from the "Choose File" input in the create event and edit event.
        :returns: directory path for attachment
        """
        try:
        # tries to create the full path of the files location and passes if
        # the directories already exist or there is no attachment
            if eventId:
                event_path = os.path.join(self.path, str(eventId))
                if not os.path.exists(event_path):
                    os.makedirs(event_path)
                file_path = os.path.join(event_path, newfile.filename)
            else:
                file_path = os.path.join(self.path, newfile.filename)
            print("*****************", file_path)
            print("^^^^^^^^^^^^^^^^^^^", event_path)
            return file_path
        except AttributeError:  # will pass if there is no attachment to save
            pass
        except FileExistsError:
            pass


    def saveFilesForEvent(self, eventId):
        """ Saves the attachment in the app/static/files/eventattachments/ directory """
        try:
            for file in self.files:
                file_path = self.getFileFullPath(eventId=eventId, newfile=file)
                if not os.path.exists(file_path):
                    isFileInEvent = EventFile.select().where(EventFile.event == eventId, EventFile.fileName == file.filename).exists()
                    if not isFileInEvent:
                        EventFile.create(event=eventId, fileName=file.filename)
                        file.save(file_path)
        except AttributeError: # will pass if there is no attachment to save
            return False
            pass

    def retrievePath(self,files, eventId = None):
        pathDict = {}
        for file in files:
            if eventId:
                file_path = os.path.join(self.path, str(eventId), file.fileName)
            else:
                file_path = os.path.join(self.path, file.fileName)
            if os.path.exists(file_path):
                pathDict[f"{eventId}_{file.fileName}"] = (file_path[3:], file)
        return pathDict

    def deleteEventFile(self, fileId, eventId):
        """
        Deletes attachmant from the app/static/files/eventattachments/ directory
        """
        try:
            file = EventFile.get_by_id(fileId)
            path = os.path.join(self.path,str(eventId), file.fileName)
            os.remove(path)
            file.delete_instance()
        except AttributeError: #passes if no attachment is selected.
            pass
