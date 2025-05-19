from datetime import datetime
import pytest
from sqlalchemy.exc import NoResultFound
from app.database.database import SessionLocal
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.grade_repository import GradeRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.subject_repository import SubjectRepository

def test_subject_repository():

    session = SessionLocal()
    try:
        # add
        name = "Python"
        subject_id = SubjectRepository.add_subject(session, name)
        subject_from_db = SubjectRepository.get_subject(session, subject_id)
        assert subject_from_db.name == name

        # edit
        name = "Lepszy Python"
        SubjectRepository.edit_subject(session, subject_id, name)
        student_from_db = SubjectRepository.get_subject(session, subject_id)
        assert student_from_db.name == name

        SubjectRepository.delete_subject(session, subject_id)
        with pytest.raises(NoResultFound):
            SubjectRepository.get_subject(session, subject_id)

        # when we delete subject do grades and attendances disappear

        student1 = StudentRepository.add_student(session, name="Grzyb", surname="Wielki", pesel="11111111111")
        subject1 = SubjectRepository.add_subject(session, "GigaPython")
        grade1 = GradeRepository.add_grade(session, student_id=student1, subject_id=subject1, form="test", worth=5)
        attendance1 = AttendanceRepository.add_attendance(session, student_id=student1, subject_id=subject1, status="present",
                                                          date_of=datetime.now())

        SubjectRepository.delete_subject(session, subject1)
        with pytest.raises(NoResultFound):
            AttendanceRepository.get_attendance(session, attendance1)

        with pytest.raises(NoResultFound):
            GradeRepository.get_grade(session, grade1)

        StudentRepository.delete_student(session, student1)
    finally:
        session.rollback()
        session.close()


