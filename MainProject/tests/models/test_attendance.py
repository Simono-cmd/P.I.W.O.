from datetime import datetime
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.grade import Grade
from app.models.failure import Failure
from app.models.subject import Subject


def test_attendance():

    att1 = Attendance(student_id = 1, subject_id=1, status="excused", date=datetime(2025, 12, 20))
    assert att1.status == "excused"