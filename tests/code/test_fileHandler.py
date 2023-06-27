import pytest
import os
from werkzeug.datastructures import FileStorage

from app import app
from app.models.attachmentUpload import AttachmentUpload
from app.models.event import Event
from app.logic.fileHandler import FileHandler

# test events
eventFileStorageObject= [FileStorage(filename= "eventfile.pdf")]

handledEventFile = FileHandler(eventFileStorageObject, eventId=15)

# test course
courseFileStorageObject= [FileStorage(filename= "coursefile.pdf")]

handledCourseFile = FileHandler(courseFileStorageObject, courseId=1)
@pytest.mark.integration
def test_getFileFullPath():
    # test event
    filePath = handledEventFile.getFileFullPath("15/" + "".join(eventFileStorageObject[0].filename))
    assert filePath == 'app/static/files/eventattachments/15/eventfile.pdf'
    
    # test course
    filePath = handledCourseFile.getFileFullPath("".join(courseFileStorageObject[0].filename))
    assert filePath == 'app/static/files/courseattachments/1/coursefile.pdf'


@pytest.mark.integration
def test_saveFiles():
    # test event
    handledEventFile.saveFiles(saveOriginalFile = Event.get_by_id(15))
    # print(AttachmentUpload.fileName)
    assert AttachmentUpload.select().where(AttachmentUpload.fileName == '15/eventfile.pdf').exists()
    
    # test course
    handledCourseFile.saveFiles()
    assert AttachmentUpload.select().where(AttachmentUpload.fileName == 'coursefile.pdf').exists()

@pytest.mark.integration
def test_recurringSaveFiles():

@pytest.mark.integration
def test_retrievePath():
    # test event
    eventfiles= AttachmentUpload.select().where(AttachmentUpload.event == 15)
    paths = handledEventFile.retrievePath(eventfiles)
    path = paths["15/eventfile.pdf"][0]
    assert path =='/static/files/eventattachments/15/eventfile.pdf'

    # test recurring event

    # test course
    coursefiles= AttachmentUpload.select().where(AttachmentUpload.course == 1)
    paths = handledCourseFile.retrievePath(coursefiles)
    path = paths["coursefile.pdf"][0]
    assert path =='/static/files/courseattachments/1/coursefile.pdf'

@pytest.mark.integration
def test_recurringSaveFiles():

@pytest.mark.integration
def test_deleteFile():
    # test file
    eventfiles= AttachmentUpload.select().where(AttachmentUpload.event == 15)
    pathDictionary = handledEventFile.retrievePath(eventfiles)
    fileId = pathDictionary["15/eventfile.pdf"][1]
    path = pathDictionary["15/eventfile.pdf"][0]
    handledEventFile.deleteFile(fileId)
    assert os.path.exists(path)==False

    # test course
    coursefiles= AttachmentUpload.select().where(AttachmentUpload.course == 1)
    pathDictionary = handledCourseFile.retrievePath(coursefiles)
    fileId = pathDictionary["coursefile.pdf"][1]
    path = pathDictionary["coursefile.pdf"][0]
    assert os.path.exists(path)==False
