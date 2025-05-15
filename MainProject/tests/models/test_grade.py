from app.models.attendance import Attendance
from app.models.student import Student
from app.models.grade import Grade
from app.models.failure import Failure
from app.models.subject import Subject

def test_grade():

    grad1 = Grade(student_id=1, subject_id=1, form="short test", worth=5)
    assert grad1.worth == 5