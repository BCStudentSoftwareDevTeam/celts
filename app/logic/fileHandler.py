import os

from flask import redirect, url_for
from app import app


class FileHandler:
    def __init__(self,attachments):
        self.attachment_file=attachments
        self.attachment_path= app.config['event']['event_attachment_path']





    def getAttachmentFullPath(self, newfile=None):
        """
        This creates the directory/path for the object from the "Choose File" input in the create event and edit event.
        :returns: directory path for attachment
        """
        try:
            # tries to create the full path of the files location and passes if
            # the directories already exist or there is no attachment
            attachmentFullPath=(os.path.join(self.attachment_path, newfile.filename))
            os.mkdir(self.attachment_path)

        except AttributeError:  # will pass if there is no attachment to save
            pass
        except FileExistsError:
            pass
        return attachmentFullPath

    def saveAttachment(self):
        """ Saves the attachment in the app/static/files/eventattachments/ directory """
        try:
            for file in self.attachment_file:
                file.save(self.getAttachmentFullPath(file)) # saves attachment in directory
        except AttributeError: # will pass if there is no attachment to save
            pass

    def deleteAttachment(self):
        """
        Deletes attachmant from the app/static/files/eventattachments/ directory
        """
        try:
            for file in self.attachment_file:
                os.remove(self.getAttachmentFullPath(file))
        except AttributeError: #passes if no attachment is selected.
            pass
    def retrievePath(self):
        pathDict={}
        for file in self.attachment_file:
            pathDict[file.fileName] = ((self.attachment_path+"/"+file.fileName)[3:], file)

        return pathDict
