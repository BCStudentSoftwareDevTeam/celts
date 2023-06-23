import os
from flask import redirect, url_for
from app import app
from app.models.attachmentUpload import AttachmentUpload

class FileHandler:
    def __init__(self,files=None, courseId=None, eventId=None):
        self.files=files
        self.path = app.config['files']['base_path']
        self.courseId = courseId
        self.eventId = eventId
        if courseId:
            self.path = os.path.join(self.path, app.config['files']['course_attachment_path'], str(courseId))
        elif eventId:
            self.path = os.path.join(self.path, app.config['files']['event_attachment_path'], str(eventId))
        try:
            os.makedirs(self.path)
        except:
            print("Directory exists.")

    def getFileFullPath(self, newfile = None):
        """
        This creates the directory/path for the object from the "Choose File" input in the create event and edit event.
        :returns: directory path for attachment
        """
        try:
            # tries to create the full path of the files location and passes if
            # the directories already exist or there is no attachment
            filePath=(os.path.join(self.path, newfile.filename))
        except AttributeError:  # will pass if there is no attachment to save
            pass
        except FileExistsError:
            pass
        return filePath

    def saveFiles(self, saveOriginalFile):
        """ Saves the attachment in the app/static/files/eventattachments/ or courseattachements/ directory """
        try:
            fileCount = 1
            for file in self.files:
                if self.eventId:
                    if fileCount:       # Checks if iterant is the first (recurring) event
                        isFileInEvent = AttachmentUpload.select().where(AttachmentUpload.event == self.eventId, AttachmentUpload.fileName == file.filename).exists()
                        if not isFileInEvent:
                            AttachmentUpload.create(event = self.eventId, fileName = file.filename)
                            file.save(self.getFileFullPath(newfile = file))
                            fileCount = 0
                            print("The lines are working effectively")
                    else:
                        isFileInEvent = AttachmentUpload.select().where(AttachmentUpload.event == self.eventId, AttachmentUpload.fileName == file.filename).exists()
                        if not isFileInEvent:
                            AttachmentUpload.create(event = self.eventId, fileName = file.filename)
                            file.save(self.getFileFullPath(newfile = file))
                            print("Code not working, help")
                elif self.courseId:
                    isFileInCourse = AttachmentUpload.select().where(AttachmentUpload.course == self.courseId, AttachmentUpload.fileName == file.filename).exists()
                    if not isFileInCourse:
                        AttachmentUpload.create(course = self.courseId, fileName = file.filename)
                        file.save(self.getFileFullPath(newfile = file)) # saves attachment in directory
        except AttributeError: # will pass if there is no attachment to save
            pass

    def retrievePath(self,files):
        pathDict={}
        for file in files:
            pathDict[file.fileName] = ((self.path+"/"+ file.fileName)[3:], file)

        return pathDict

    def deleteFile(self, fileId):
        """
        Deletes attachmant from the app/static/files/eventattachments/ or courseattachments/ directory
        """
        try:
            file = AttachmentUpload.get_by_id(fileId)
            path = os.path.join(self.path, file.fileName)
            os.remove(path)
            file.delete_instance()
        except AttributeError: #passes if no attachment is selected.
            pass