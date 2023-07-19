import pytest 
from flask import g 
from app import app
from app.models import mainDB
from app.models.term import Term 
from app.models.course import Course
from app.models.courseParticipant import CourseParticipant
from app.logic.serviceLearningCoursesData import parseUploadedFile, pushDataToDatabase

@pytest.mark.integration
def test_PushDataToDatabase():
    
    with mainDB.atomic() as transaction:
        listOfParticipants = [[['CSC 226', 'CSC 226'], 'Fall 2020', 'Karina Agliullova', 'Ebenezer Ayisi'],
            [['HIS 236', 'HIS 236'], 'Fall 2020', 'Finn Bledsoe', 'Alex Bryant'],
            [['CSC 450', 'CSC 450'], 'Spring 2020', 'Sreynit Khatt', 'Sandesh Lamichhane'],
            [['CSC 650', 'CSC 650'],'Summer 2021', 'Liberty Mupotsa', 'Zach Neill'], 
            [['MAT 450', 'MAT 450'], 'Fall 2019', 'Tyler Parton', 'Ala Qasem']]

        listOfStudentsBnumber= [{'bnumber': 'B00759117', 'student_name': 'KarinaAgliullova'}, 
            {'bnumber': 'B00739736', 'student_name': 'EbenezerAyisi'}, 
            {'bnumber': 'B00776544', 'student_name': 'FinnBledsoe'},
            {'bnumber': 'B00708826', 'student_name': 'AlexBryant'}, 
            {'bnumber': 'B00759107', 'student_name': 'SreynitKhatt'},
            {'bnumber': 'B00733993', 'student_name': 'SandeshLamichhane'},  
            {'bnumber': 'B00741640', 'student_name': 'LibertyMupotsa'},
            {'bnumber': 'B00751864', 'student_name': 'ZachNeill'}, 
            {'bnumber': 'B00751360', 'student_name': 'TylerParton'},
            {'bnumber': 'B00000000', 'student_name': 'AlaQasem'}]

        assert Term.get_or_none(Term.description =="Fall 2019") == None
        assert Term.get_or_none(Term.description == "Spring 2020") == None

        assert Course.get_or_none(Course.courseAbbreviation == "CSC 226") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "HIS 236") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "CSC 650") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "MAT 450") == None 
        assert Course.get_or_none(Course.courseAbbreviation == "CSC 450") == None 

        assert CourseParticipant.get_or_none(CourseParticipant.courseAbbreviation == " CS") == None

        with app.app_context():
            g.current_user="ramsayb2" 
            pushDataToDatabase(listOfParticipants,listOfStudentsBnumber)

        termGetMethod= Term.get_or_none(Term.description == "Fall 2019")
        assert termGetMethod.description== "Fall 2019"

        termGetMethod= Term.get_or_none(Term.description == "Spring 2020")
        assert termGetMethod.description== "Spring 2020"

        assert CourseParticipant.get_or_none(CourseParticipant. == " CS") == None 
        transaction.rollback()

@pytest.mark.integration
def test_valid_file():
    valid_file_path = 'tests/parseUpload_ValidTest.xlsx'  
    result = parseUploadedFile(valid_file_path)
    assert isinstance(result, tuple)
    assert len(result) == 4
    previewParticipants, listOfStudentsBnumber, errorFlag, termDictionary = result

    assert not errorFlag
    assert isinstance(previewParticipants, list)
    assert isinstance(listOfStudentsBnumber, list)
    assert isinstance(termDictionary, dict)

@pytest.mark.integration
def test_invalid_file():
    invalid_file_path = 'tests/parseUpload_InvalidTest.xlsx'  
    result = parseUploadedFile(invalid_file_path)
    assert isinstance(result, tuple)
    assert len(result) == 4
    previewParticipants, listOfStudentsBnumber, errorFlag, termDictionary = result

    assert errorFlag == False
    assert len(previewParticipants) == 5
    assert len(listOfStudentsBnumber) == 9
    assert len(termDictionary) == 4




