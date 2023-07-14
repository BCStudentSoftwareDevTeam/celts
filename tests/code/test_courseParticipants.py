
import pytest 

from app.logic.serviceLearningCoursesData import parseUploadedFile



@pytest.mark.integration
def testCourseParticipants():
    testDocPath= './app/static/files/Test Document 2.xlsx'
    expectedDictionary = [
        ['CSC 226', 'Fall 2020', 'Gaston Jarju', 'Eben Ezer'],
        ['HIS 236', 'Fall 2020', 'Ali Ramazani', 'Gertrude Mbewe'],
        ['CSC 450', 'Spring 2026', 'Fleur Gahimbare', 'Isaac Narteh'],
        ['CSC 650', 'Summer 2024', 'Anh Ngo', 'Claudia Pulido'],
        ['MAT 450', 'May 2025', 'Alisha Supeidi', 'Erika Arvizu']
        ]
        
    testUpload = parseUploadedFile(testDocPath)
    assert expectedDictionary == testUpload[0]



