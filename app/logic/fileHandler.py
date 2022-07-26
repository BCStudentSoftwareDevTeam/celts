import os

from flask import redirect, url_for
from app import app
from app.models.eventFile import EventFile

class FileHandler:
    def __init__(self,files=None):
        self.files=files
        self.path= app.config['event']['event_attachment_path']





    def getFileFullPath(self, eventId=None, newfile = None):
        """
        This creates the directory/path for the object from the "Choose File" input in the create event and edit event.
        :returns: directory path for attachment
        """
        try:
            # tries to create the full path of the files location and passes if
            # the directories already exist or there is no attachment
            if eventId:
                filePath=(os.path.join(self.path, str(eventId), newfile.filename))
                os.mkdir(self.path+"/"+ str(eventId))
            else:
                filePath=(os.path.join(self.path, newfile.filename))
                os.mkdir(self.path+"/"+ str(eventId))
        except AttributeError:  # will pass if there is no attachment to save
            pass
        except FileExistsError:
            pass
        return filePath

    def saveFile(self, eventId):
        """ Saves the attachment in the app/static/files/eventattachments/ directory """
        try:
            for file in self.files:
                EventFile.create(event = eventId, fileName = file.filename)
                file.save(self.getFileFullPath(eventId, file)) # saves attachment in directory
        except AttributeError: # will pass if there is no attachment to save
            return False
            pass

    def deleteFile(self,fileId, eventId):
        """
        Deletes attachmant from the app/static/files/eventattachments/ directory
        """
        try:
            File = EventFile.get_by_id(fileId)
            path = os.path.join(self.path,eventId, File.fileName)
            os.remove(path)
            File.delete_instance()
        except AttributeError: #passes if no attachment is selected.
            pass

    def retrievePath(self):
        pathDict={}
        for file in self.files:
            pathDict[file.fileName] = ((self.path+"/"+file.fileName)[3:], file)
        print(pathDict)
        return pathDict
