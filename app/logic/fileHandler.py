import os
from flask import redirect, url_for
from app import app
from app.models.attachmentUpload import AttachmentUpload
from app.models.program import Program
import glob

class FileHandler:
    def __init__(self, files=None, courseId=None, eventId=None, programId=None):
        self.files = files 
        self.path = app.config['files']['base_path']
        self.path1 = app.config['files']['image_path']    
        self.courseId = courseId
        self.eventId = eventId
        self.programId = programId
        if courseId:
            self.path = os.path.join(self.path, app.config['files']['course_attachment_path'], str(courseId))
        elif eventId:
            self.path = os.path.join(self.path, app.config['files']['event_attachment_path'])
        elif programId:
            self.path1 = os.path.join(self.path1, app.config['files']['landing_page_path']) 
    def makeDirectory(self):
        try:
            extraDir = str(self.eventId) if self.eventId else ""
            os.makedirs(os.path.join(self.path, extraDir))
        except OSError as e:
            if e.errno != 17:
                print(f'Fail to create directory: {e}')
                raise e
    
    def getFileFullPath(self, newfilename=''):
        try:
            filePath = (os.path.join(self.path1, newfilename))
        except AttributeError:
            pass
        except FileExistsError:
            pass
        return filePath

    def saveFiles(self, saveOriginalFile=None):
      
        try: 
            if not isinstance(self.files, list):
                self.files = [self.files]          
            for file in self.files:

                saveFileToFilesystem = None

                if self.eventId:
                    attachmentName = str(saveOriginalFile.id) + "/" + file.filename
                    isFileInEvent = AttachmentUpload.select().where(AttachmentUpload.event_id == self.eventId,
                                                                    AttachmentUpload.fileName == attachmentName).exists()
                    if not isFileInEvent:
                        AttachmentUpload.create(event=self.eventId, fileName=attachmentName)
                        if saveOriginalFile and saveOriginalFile.id == self.eventId:
                            saveFileToFilesystem = attachmentName
                elif self.courseId:
                    isFileInCourse = AttachmentUpload.select().where(AttachmentUpload.course == self.courseId, AttachmentUpload.fileName == file.filename).exists()
                    if not isFileInCourse:
                        AttachmentUpload.create(course=self.courseId, fileName=file.filename)
                        saveFileToFilesystem = file.filename
                elif self.programId:
                    isFileInProgram = AttachmentUpload.select().where(AttachmentUpload.program == self.programId, AttachmentUpload.fileName == file.filename).exists()
                    if not  isFileInProgram:
                        AttachmentUpload.create(program=self.programId, fileName=file.filename)                      
                        name = Program.get(Program.id == self.programId)
                        file_type = file.filename.split('.')[1] 
                        current_programName = f"{str(name.programName)}.{file_type}"
                        pattern = '*' + str(name.programName) + '*'
                        
                        full_pattern = os.path.join(self.path1, pattern)
                        files_to_delete = glob.glob(full_pattern)
                       

                        for  file_path in files_to_delete:
                                os.remove(file_path)
                        saveFileToFilesystem = current_programName
                else:
                    saveFileToFilesystem = file.filename
                if saveFileToFilesystem:
                    self.makeDirectory()
                    file.save(self.getFileFullPath(newfilename=saveFileToFilesystem))

        except AttributeError:
            pass

    def retrievePath(self, files):
        pathDict = {}
        for file in files:
            pathDict[file.fileName] = ((self.path + "/" + file.fileName)[3:], file)
        return pathDict

    def deleteFile(self, fileId):
        file = AttachmentUpload.get_by_id(fileId)
        file.delete_instance()
        if not AttachmentUpload.select().where(AttachmentUpload.fileName == file.fileName).exists():
            path = os.path.join(self.path, file.fileName)
            os.remove(path)

    def changeDisplay(self, fileId, isDisplayed):
        file = AttachmentUpload.get_by_id(fileId)
        
        # Uncheck all other checkboxes for the same event
        AttachmentUpload.update(isDisplayed=False).where(AttachmentUpload.event == file.event).execute()

        # Check the selected checkbox
        AttachmentUpload.update(isDisplayed=isDisplayed).where(AttachmentUpload.id == fileId).execute()
        return ""
