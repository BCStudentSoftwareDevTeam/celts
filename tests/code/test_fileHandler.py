import pytest
import os
from werkzeug.datastructures import FileStorage



from app import app
from app.models import mainDB
from dateutil import parser
from app.models.user import User
from flask import g
from app.logic.events import attemptSaveEvent


from app.models.program import Program
from app.models.attachmentUpload import AttachmentUpload
from app.models.event import Event
from app.logic.fileHandler import FileHandler

# test events
eventFileStorageObject= [FileStorage(filename= "eventfile.pdf")]

handledEventFile = FileHandler(eventFileStorageObject, eventId=15)

# eventFileStorageObjectRecurring= [FileStorage(filename= "eventfile.pdf")]

handledEventFileRecurring = FileHandler(eventFileStorageObject, eventId=16)

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
    
    # test saving 2nd event in a hypothetical recurring series
    handledEventFileRecurring.saveFiles(saveOriginalFile = Event.get_by_id(15))
    assert AttachmentUpload.select().where(AttachmentUpload.event_id == 16, AttachmentUpload.fileName == '15/eventfile.pdf').exists()

    # test course
    handledCourseFile.saveFiles()
    assert AttachmentUpload.select().where(AttachmentUpload.fileName == 'coursefile.pdf').exists()

@pytest.mark.integration
def test_retrievePath():
    # test event
    eventfiles= AttachmentUpload.select().where(AttachmentUpload.event == 15)
    paths = handledEventFile.retrievePath(eventfiles)
    path = paths["15/eventfile.pdf"][0]
    assert path =='/static/files/eventattachments/15/eventfile.pdf'

    # test recurring event
    # this tests that the recurring events are referencing the same file directory as the first event.
    eventfiles= AttachmentUpload.select().where(AttachmentUpload.event == 16)
    paths = handledEventFile.retrievePath(eventfiles)
    path = paths["15/eventfile.pdf"][0]
    assert path =='/static/files/eventattachments/15/eventfile.pdf'

    # test course
    coursefiles= AttachmentUpload.select().where(AttachmentUpload.course == 1)
    paths = handledCourseFile.retrievePath(coursefiles)
    path = paths["coursefile.pdf"][0]
    assert path =='/static/files/courseattachments/1/coursefile.pdf'

@pytest.mark.integration
def test_deleteFile():
    
    # test file
    eventfiles= AttachmentUpload.select().where(AttachmentUpload.event == 15)
    pathDictionary = handledEventFile.retrievePath(eventfiles)

    pathDictTest = handledEventFile.getFileFullPath("15/eventfile.pdf")

    path = pathDictionary["15/eventfile.pdf"][0]
    assert os.path.exists(pathDictTest)==True, f"Path {path} does not exist"

    firstevent = AttachmentUpload.get(AttachmentUpload.event == 15)
    handledEventFile.deleteFile(firstevent.id)
    assert os.path.exists(pathDictTest)==True
 
    secondevent = AttachmentUpload.get(AttachmentUpload.event == 16)
    handledEventFile.deleteFile(secondevent.id)
    assert os.path.exists(pathDictTest)==False

    # test recurring events
    

    # test course
    coursefiles= AttachmentUpload.select().where(AttachmentUpload.course == 1)
    pathDictionary = handledCourseFile.retrievePath(coursefiles)
    fileId = pathDictionary["coursefile.pdf"][1]
    path = pathDictionary["coursefile.pdf"][0]
    assert os.path.exists(path)==False
