from app.models.attendance import Attendance
from app.models.student import Student
from app.models.grade import Grade
from app.models.failure import Failure
from app.models.subject import Subject

def test_student_initialization():
    student = Student(id = 1, name = "Jan", surname = "Kowalski", pesel = "12345678901")
    assert student.id == 1
    assert student.name == "Jan"