import os

from flask import redirect, url_for
from app import app
from app.models.eventFile import EventFile

class FileHandler:
    def __init__(self,attachments=None):
        self.attachment_files=attachments
        self.attachment_path= app.config['event']['event_attachment_path']





    def getAttachmentFullPath(self, eventId, newfile = None):
        """
        This creates the directory/path for the object from the "Choose File" input in the create event and edit event.
        :returns: directory path for attachment
        """
        try:
            # tries to create the full path of the files location and passes if
            # the directories already exist or there is no attachment
            attachmentFullPath=(os.path.join(self.attachment_path, str(eventId), newfile.filename))
            os.mkdir(self.attachment_path+"/"+ str(eventId))

        except AttributeError:  # will pass if there is no attachment to save
            pass
        except FileExistsError:
            pass
        return attachmentFullPath

    def saveAttachment(self, eventId):
        """ Saves the attachment in the app/static/files/eventattachments/ directory """

        try:
            for file in self.attachment_files:

                EventFile.create(event = eventId, fileName = file.filename)
                file.save(self.getAttachmentFullPath(eventId, file)) # saves attachment in directory
        except AttributeError: # will pass if there is no attachment to save
            pass
    def deleteAttachment(self, fileId, eventId):
        """
        Deletes attachmant from the app/static/files/eventattachments/ directory
        """
        try:
            File = EventFile.get_by_id(fileId)
            path = os.path.join( self.attachment_path,eventId, File.fileName)
            os.remove(path)
            File.delete_instance()
        except AttributeError: #passes if no attachment is selected.
            pass
    def retrievePath(self):
        pathDict={}
        for file in self.attachment_files:
            pathDict[file.fileName] = ((self.attachment_path+"/"+file.fileName)[3:], file)

        return pathDict
