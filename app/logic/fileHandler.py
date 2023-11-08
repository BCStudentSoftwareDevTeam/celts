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
            # eventID is not included in the path, because it is now a part of the attachment filename.
            self.path = os.path.join(self.path, app.config['files']['event_attachment_path'])
        
    def makeDirectory(self):
        # This creates a directory. 
        # Created to remove duplicates when an event is recurring.
        try:
            extraDir = str(self.eventId) if self.eventId else ""
            os.makedirs(os.path.join(self.path, extraDir))
        # Error 17 Occurs when we try to create a directory that already exists
        except OSError as e:
            if e.errno != 17:
                print(f'Fail to create directory: {e}')
                raise e
                
    def getFileFullPath(self, newfilename = ''):
        """
        This creates the directory/path for the object from the "Choose File" input in the create event and edit event.
        :returns: directory path for attachment
        """

        # Added the eventID of the first recurring event to track the file path for subsequent recurring events.
        try:
            # tries to create the full path of the files location and passes if
            # the directories already exist or there is no attachment
            filePath=(os.path.join(self.path, newfilename))
        except AttributeError:  # will pass if there is no attachment to save
            pass
        except FileExistsError:
            pass
  
        return filePath

    def saveFiles(self, saveOriginalFile=None):
        """ Saves the attachment in the app/static/files/eventattachments/ or courseattachements/ directory """
        try:
            for file in self.files:
                saveFileToFilesystem = None
                if self.eventId:
                    attachmentName = str(saveOriginalFile.id) + "/" +  file.filename

                    # isFileInEvent checks if the attachment exists in the database under that eventId and filename.
                    isFileInEvent = AttachmentUpload.select().where(AttachmentUpload.event_id == self.eventId,
                                                                    AttachmentUpload.fileName == attachmentName).exists()
                    if not isFileInEvent:
                        AttachmentUpload.create(event = self.eventId, fileName = attachmentName)

                        # Only save the file if our event is on its own, or the first of a recurring series
                        if saveOriginalFile and saveOriginalFile.id == self.eventId:
                            saveFileToFilesystem = attachmentName
 
                elif self.courseId:
                    isFileInCourse = AttachmentUpload.select().where(AttachmentUpload.course == self.courseId, AttachmentUpload.fileName == file.filename).exists()
                    if not isFileInCourse:
                        AttachmentUpload.create(course = self.courseId, fileName = file.filename)
                        saveFileToFilesystem = file.filename
                
                if saveFileToFilesystem:
                    self.makeDirectory()
                    file.save(self.getFileFullPath(newfilename = saveFileToFilesystem))        
                        
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
        file = AttachmentUpload.get_by_id(fileId)
        file.delete_instance()

        # checks if there are other instances with the same filename in the AttachmentUpload table
        if not AttachmentUpload.select().where(AttachmentUpload.fileName == file.fileName).exists():
            path = os.path.join(self.path, file.fileName)
            os.remove(path)
    
    def changeDisplay(self, fileId):
        file = AttachmentUpload.get_by_id(fileId)
        AttachmentUpload.update(isDisplayed=False).where(AttachmentUpload.event == file.event, AttachmentUpload.isDisplayed==True).execute()
        AttachmentUpload.update(isDisplayed=True).where(AttachmentUpload.id == fileId).execute()
        return "" 
