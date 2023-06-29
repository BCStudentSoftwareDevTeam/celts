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
    # creates recurring events for transaction
    # eventInfo =  { 'isTraining':'on', 'isRecurring':False, 'recurringId':None,
    #             'startDate': '2021-12-12',
    #             'rsvpLimit': None,
    #             'endDate':'2022-06-12', 'location':"a big room",
    #             'timeEnd':'09:00 PM', 'timeStart':'06:00 PM',
    #             'description':"Empty Bowls Spring 2021",
    #             'name':'Attempt Save Test','term':1,'contactName':"Garrett D. Clark",
    #             'contactEmail': 'boorclark@gmail.com'}
    # eventInfo['program'] = Program.get_by_id(1)
            # eventInfo['eventAttachment'] = 'recurringEvent.pdf'
    eventInfo =  { 'isTraining':'on', 'isRecurring':False, 'recurringId':None,
                'startDate': '2021-12-12',
                'rsvpLimit': None,
                'endDate':'2022-06-12', 'location':"a big room",
                'timeEnd':'09:00 PM', 'timeStart':'06:00 PM',
                'description':"Empty Bowls Spring 2021",
                'name':'bloo','term':1,'contactName':"Garrett D. Clark",
                'contactEmail': 'boorclark@gmail.com'}
    eventInfo['program'] = Program.get_by_id(1)



    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = User.get_by_id("ramsayb2")
            createdEvents = attemptSaveEvent(eventInfo)
            bla  = Event.select().where(Event.name == "bloo")
            print([food.isRecurring for food in bla])
            assert AttachmentUpload.select().where(AttachmentUpload.fileName == 'recurringEvent.pdf').exists()

            transaction.rollback()
        
        # saves recurring events

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
