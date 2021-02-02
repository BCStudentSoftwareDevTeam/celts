import pytest
from app.logic.tracy import Tracy
from app.logic.tracy import InvalidQueryException

@pytest.fixture(scope='class')
def tracy(request):
    return Tracy()

@pytest.mark.usefixtures("tracy")
class Test_Tracy:

    @pytest.mark.unit
    def test_init(self, tracy):
        assert True

    @pytest.mark.integration
    def test_getStudents(self, tracy):
        students = tracy.getStudents()
        assert ['Alex','Elaheh','Guillermo','Jeremiah','Kat'] == [s.FIRST_NAME for s in students]
        assert ['212','718','300','420','420'] == [s.STU_CPO for s in students]

    @pytest.mark.integration
    def test_getStudentFromBNumber(self, tracy):
        student = tracy.getStudentFromBNumber("B00734292")
        assert 'Guillermo' == student.FIRST_NAME

        student = tracy.getStudentFromBNumber("  B00734292")
        assert 'Guillermo' == student.FIRST_NAME

        student = tracy.getStudentFromBNumber("B00888329  ")
        assert 'Jeremiah' == student.FIRST_NAME

        with pytest.raises(InvalidQueryException):
            student = tracy.getStudentFromBNumber("B0000000")

        with pytest.raises(InvalidQueryException):
            student = tracy.getStudentFromBNumber(17)

    @pytest.mark.integration
    def test_getStudentFromEmail(self, tracy):
        student = tracy.getStudentFromEmail("cruzg@berea.edu")
        assert 'Guillermo' == student.FIRST_NAME

        with pytest.raises(InvalidQueryException):
            student = tracy.getStudentFromEmail("jimmyjoe@place.biz")

        with pytest.raises(InvalidQueryException):
            student = tracy.getStudentFromEmail(17)

    @pytest.mark.integration
    def test_getSupervisors(self, tracy):
        supervisors = tracy.getSupervisors()
        assert ['Alex','Brian','Jan','Jasmine','Mario','Megan','Scott'] == [s.FIRST_NAME for s in supervisors]
        assert ['420','6305','6301','6301','6302','6303','6300'] == [s.CPO for s in supervisors]

    @pytest.mark.integration
    def test_getSupervisorFromID(self, tracy):
        supervisor = tracy.getSupervisorFromID("B1236237")
        assert 'Megan' == supervisor.FIRST_NAME

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromID("eleven")

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromID(17)

    @pytest.mark.integration
    def test_getSupervisorFromEmail(self, tracy):
        supervisor = tracy.getSupervisorFromEmail("nakazawam@berea.edu")
        assert 'Mario' == supervisor.FIRST_NAME

        supervisor = tracy.getSupervisorFromEmail("heggens@berea.edu")
        assert 'Scott' == supervisor.FIRST_NAME

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromEmail("nakazawamasdfd.com")

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromEmail(17)

    @pytest.mark.integration
    def test_getPositionsFromDepartment(self, tracy):
        positions = tracy.getPositionsFromDepartment("2114","6740")

        assert ['S61408','S61407','S61421','S61419'] == [p.POSN_CODE for p in positions]

        positions = tracy.getPositionsFromDepartment("2114","0000")
        assert [] == [p.POSN_CODE for p in positions]

    @pytest.mark.integration
    def test_getDepartments(self, tracy):
        departments = tracy.getDepartments()
        assert ['Biology','Computer Science','Mathematics','Technology and Applied Design'] == [d.DEPT_NAME for d in departments]
        assert '2107' == departments[0].ORG
        assert '6740' == departments[0].ACCOUNT

    @pytest.mark.integration
    def test_getPositionFromCode(self, tracy):
        position = tracy.getPositionFromCode("S61427")
        assert 'Teaching Associate' == position.POSN_TITLE
        assert '2' == position.WLS

        with pytest.raises(InvalidQueryException):
            position = tracy.getPositionFromCode("eleven")

        with pytest.raises(InvalidQueryException):
            position = tracy.getPositionFromCode(17)

    @pytest.mark.integration
    def test_getSupervisorsFromUserInput(self, tracy):
        supervisor = tracy.getSupervisorsFromUserInput("Jan Pearce")
        assert "Jan" == supervisor[0].FIRST_NAME
        assert 1 == len(supervisor)

        supervisor = tracy.getSupervisorsFromUserInput("heggen")
        assert "Scott" == supervisor[0].FIRST_NAME
        assert 1 == len(supervisor)

        supervisor = tracy.getSupervisorsFromUserInput("Peter Parker")
        assert supervisor != True
        assert 0 == len(supervisor)

    @pytest.mark.integration
    def test_getStudentsFromUserInput(self, tracy):
        students = tracy.getStudentsFromUserInput("Guillermo")
        assert "Guillermo" == students[0].FIRST_NAME
        assert 1 == len(students)

        students = tracy.getStudentsFromUserInput("Adams")
        assert  2 == len(students)
        assert "Adams" == students[1].LAST_NAME

        students = tracy.getSupervisorsFromUserInput("John Smith")
        assert students != True
        assert 0 == len(students)

    @pytest.mark.integration
    def test_checkStudentOrSupervisor(self, tracy):
        user = tracy.checkStudentOrSupervisor("cruzg")
        assert "Student" == user

        user = tracy.checkStudentOrSupervisor("heggens")
        assert "Supervisor" == user

        with pytest.raises(InvalidQueryException):
            user = tracy.checkStudentOrSupervisor("smith")
