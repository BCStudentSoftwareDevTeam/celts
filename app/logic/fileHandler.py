import os

from flask import redirect, url_for
from app import app
from app.models.eventFile import EventFile

class FileHandler:
    def __init__(self,attachments):
        self.attachment_files=attachments
        self.attachment_path= app.config['event']['event_attachment_path']





    def getAttachmentFullPath(self, eventId=None, newfile = None):
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
            print("TryTryTryTryTryTryTry")
            print(self.attachment_files)
            for file in self.attachment_files:

                EventFile.create(event = eventId, fileName = file.filename)
                print("pass Table Creation")
                file.save(self.getAttachmentFullPath(eventId, file)) # saves attachment in directory
        except AttributeError: # will pass if there is no attachment to save
            print("AttributeError")
            pass
    def deleteAttachment(self):
        """
        Deletes attachmant from the app/static/files/eventattachments/ directory
        """
        try:
            for file in self.attachment_files:
                os.remove(self.getAttachmentFullPath(file))
        except AttributeError: #passes if no attachment is selected.
            pass
    def retrievePath(self):
        pathDict={}
        for file in self.attachment_files:
            pathDict[file.fileName] = ((self.attachment_path+"/"+file.fileName)[3:], file)

        return pathDict
