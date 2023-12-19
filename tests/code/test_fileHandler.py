import pytest
import os
import shutil
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

# creates base object for events tests
eventFileStorageObject= [FileStorage(filename= "eventfile.pdf")]

handledEventFile = FileHandler(eventFileStorageObject, eventId=15)

handledEventFileRecurring = FileHandler(eventFileStorageObject, eventId=16)

# creates base object for course tests
courseFileStorageObject= [FileStorage(filename= "coursefile.pdf")]

handledCourseFile = FileHandler(courseFileStorageObject, courseId=1)
@pytest.mark.integration
def test_getFileFullPath():
    # test event
    filePath = handledEventFile.getFileFullPath("15/" + "".join(eventFileStorageObject[0].filename))
    assert filePath == 'app/static/files/eventattachments/15/eventfile.pdf'
    
    # test course
    filePath = handledCourseFile.getFileFullPath(courseFileStorageObject[0].filename)
    assert filePath == 'app/static/files/courseattachments/1/coursefile.pdf'

@pytest.mark.integration
def test_makingdirectory():
    #Testing that the file is created and it exists
    event_id = 90
    path = 'app/static/files/eventattachments/'
    # Ensure the directory does not exist before calling makeDirectory
    try:
       os.rmdir('app/static/files/eventattachments/90')
    except OSError as e:
       shutil.rmtree('app/static/files/eventattachments/90', ignore_errors = True)
    assert os.path.exists(os.path.join(path, str(event_id))) == False
    # Creating directory and making sure it exist
    eventFileStorage= [FileStorage(filename= "eventfile.pdf")]
    handledEventAttachment = FileHandler(eventFileStorage, eventId= 90)
    handledEventAttachment.makeDirectory()
    
    handledEventAttachment.makeDirectory()
    assert os.path.exists('app/static/files/eventattachments/90') == True
    # Deleting the directory
    os.rmdir('app/static/files/eventattachments/90')
    
    
@pytest.mark.integration
def test_saveFiles():
    with mainDB.atomic() as transaction:
        # test event
        handledEventFile.saveFiles(saveOriginalFile = Event.get_by_id(15))
        
        assert AttachmentUpload.select().where(AttachmentUpload.fileName == '15/eventfile.pdf').exists()
        
        # test saving 2nd event in a hypothetical recurring series
        handledEventFileRecurring.saveFiles(saveOriginalFile = Event.get_by_id(15))
        assert AttachmentUpload.select().where(AttachmentUpload.event_id == 16, AttachmentUpload.fileName == '15/eventfile.pdf').exists()
        assert 1 == AttachmentUpload.select().where(AttachmentUpload.event_id == 16, AttachmentUpload.fileName == '15/eventfile.pdf').count()
        
        handledEventFileRecurring.saveFiles(saveOriginalFile = Event.get_by_id(15))
        assert 1 == AttachmentUpload.select().where(AttachmentUpload.event_id == 16, AttachmentUpload.fileName == '15/eventfile.pdf').count()

        # test course
        handledCourseFile.saveFiles()
        assert AttachmentUpload.select().where(AttachmentUpload.fileName == 'coursefile.pdf').exists()

        # removes saved paths from file directory
        os.remove(handledEventFile.getFileFullPath('15/eventfile.pdf'))
        os.remove(handledCourseFile.getFileFullPath('coursefile.pdf'))
        
        transaction.rollback()

@pytest.mark.integration
def test_retrievePath():
    with mainDB.atomic() as transaction:

        # uploads attachments for course test to the database using the transaction
        AttachmentUpload.create(course=1, fileName= 'coursefile.pdf')

        # uploads attachments for events tests to the database using the transaction
        AttachmentUpload.create(event=15, fileName= '15/eventfile.pdf')

        AttachmentUpload.create(event=16, fileName= '15/eventfile.pdf')


        # test event
        eventfiles= AttachmentUpload.select().where(AttachmentUpload.event == 15)
        paths = handledEventFile.retrievePath(eventfiles)
        path = paths['15/eventfile.pdf'][0]
        assert path =='/static/files/eventattachments/15/eventfile.pdf'

        # test recurring event
        # this tests that the recurring events are referencing the same file directory as the first event.
        eventfiles= AttachmentUpload.select().where(AttachmentUpload.event == 16)
        paths = handledEventFile.retrievePath(eventfiles)
        path = paths['15/eventfile.pdf'][0]
        assert path =='/static/files/eventattachments/15/eventfile.pdf'

        # test course
        coursefiles= AttachmentUpload.select().where(AttachmentUpload.course == 1)
        paths = handledCourseFile.retrievePath(coursefiles)
        path = paths["coursefile.pdf"][0]
        assert path =='/static/files/courseattachments/1/coursefile.pdf'

        transaction.rollback()

@pytest.mark.integration
def test_deleteFile():
    with mainDB.atomic() as transaction:
        # creates file in event file directory for deletion
        handledEventFile.saveFiles(saveOriginalFile = Event.get_by_id(15))

        # creates a second file to simulate recurring events
        handledEventFileRecurring.saveFiles(saveOriginalFile = Event.get_by_id(15))
        
        # creates a course file for deletion
        handledCourseFile.saveFiles()

        # delete events
        path = handledEventFile.getFileFullPath("15/eventfile.pdf")

        # if multiple event attachments reference the same path, the path is only removed after the final referencing instance has been deleted.
        firstevent = AttachmentUpload.get(AttachmentUpload.event == 15)
        handledEventFile.deleteFile(firstevent.id)
        assert os.path.exists(path)==True
    
        secondevent = AttachmentUpload.get(AttachmentUpload.event == 16)
        handledEventFile.deleteFile(secondevent.id)
        assert os.path.exists(path)==False

        # delete courses
        coursefile = AttachmentUpload.get(AttachmentUpload.course == 1)
        
        path = handledCourseFile.getFileFullPath('coursefile.pdf')

        handledCourseFile.deleteFile(coursefile.id)
        
        assert os.path.exists(path)==False
@pytest.mark.integration
def test_displayFile():
    with mainDB.atomic() as transaction:
        # create two image files to test the display function 
        image1 = AttachmentUpload.create(event=15, fileName= 'coverImage.png')
        image2 = AttachmentUpload.create(event=15, fileName= 'coverImage.svg')

        eventfile = FileHandler(eventId=1)

        # display image1 as an event cover 
        eventfile.changeDisplay(image1)

        assert AttachmentUpload.get_by_id(image1).isDisplayed ==True
        assert AttachmentUpload.get_by_id(image2).isDisplayed ==False

        # display image2 as an event cover 
        eventfile.changeDisplay(image2)
        assert AttachmentUpload.get_by_id(image2).isDisplayed ==True
        assert AttachmentUpload.get_by_id(image1).isDisplayed ==False

        transaction.rollback()




        

