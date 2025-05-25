from datetime import datetime
import pytest
from sqlalchemy.exc import NoResultFound
from MainProject.app.database.database import SessionLocal
from MainProject.app.repositories.attendance_repository import AttendanceRepository
from MainProject.app.repositories.student_repository import StudentRepository
from MainProject.app.repositories.subject_repository import SubjectRepository


def test_attendance_repository():

    session = SessionLocal()
    try:
        #add
        name = "Maciej"
        surname = "Tomaszewski"
        pesel = "14205914328"
        subject_name = "Test3"
        status = "absent"
        date = datetime(2025, 11, 11, 22, 22)

        student_id = StudentRepository.add_student(session, name, surname, pesel)
        subject_id = SubjectRepository.add_subject(session, subject_name)
        attendance_id = AttendanceRepository.add_attendance(session, student_id=student_id, subject_id=subject_id, status=status, date_of=date)
        attendance = AttendanceRepository.get_attendance(session, attendance_id)

        assert attendance is not None
        assert attendance.status == status
        assert attendance.date == date

        #edit
        status = "late"
        AttendanceRepository.edit_attendance(session, attendance_id=attendance_id, status=status)
        attendance = AttendanceRepository.get_attendance(session, attendance_id)

        assert attendance is not None
        assert attendance.status == status

        StudentRepository.delete_student(session, student_id)
        SubjectRepository.delete_subject(session, subject_id)
        # attendance is being deleted automatically

        with pytest.raises(NoResultFound):
            StudentRepository.get_student(session, student_id)

        with pytest.raises(NoResultFound):
            SubjectRepository.get_subject(session, subject_id)

        with pytest.raises(NoResultFound):
            AttendanceRepository.get_attendance(session, attendance_id)
    finally:
        session.rollback()
        session.close()