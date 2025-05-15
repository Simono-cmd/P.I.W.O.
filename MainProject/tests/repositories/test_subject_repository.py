from datetime import datetime
from this import s
import pytest
from sqlalchemy.exc import NoResultFound
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.grade import Grade
from app.models.failure import Failure
from app.models.subject import Subject
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.grade_repository import GradeRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.subject_repository import SubjectRepository


def test_subject_repository():

    #session =

    # add
    name = "Python"
    subject_id = SubjectRepository.add_subject(name)
    subject_from_db = SubjectRepository.get_subject(subject_id)
    assert subject_from_db.name == name

    # edit
    name = "Lepszy Python"
    SubjectRepository.edit_subject(subject_id, name)
    student_from_db = SubjectRepository.get_subject(subject_id)
    assert student_from_db.name == name

    SubjectRepository.delete_subject(subject_id)
    with pytest.raises(NoResultFound):
        SubjectRepository.get_subject(subject_id)




    #when we delete subject do grades and attendances disappear

    student1 = StudentRepository.add_student(name="Grzyb", surname="Wielki", pesel="11111111111")
    subject1=SubjectRepository.add_subject("GigaPython")
    grade1= GradeRepository.add_grade(student_id=student1, subject_id=subject1, form="test", worth=5)
    attendance1=AttendanceRepository.add_attendance(student_id=student1, subject_id=subject1, status="present", date=datetime.now())

    print(StudentRepository.get_student(student1))
    print(AttendanceRepository.get_attendance(attendance1))
    print(GradeRepository.get_grade(grade1))

    SubjectRepository.delete_subject(subject1)

    with pytest.raises(NoResultFound):
        AttendanceRepository.get_attendance(attendance1)

    with pytest.raises(NoResultFound):
        GradeRepository.get_grade(grade1)

    StudentRepository.delete_student(student1)
