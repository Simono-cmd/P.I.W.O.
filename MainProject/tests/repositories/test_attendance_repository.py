from datetime import datetime

import pytest
from sqlalchemy.exc import NoResultFound

from app.database.database import SessionLocal
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.subject_repository import SubjectRepository


def test_attendance_repository():

    session = SessionLocal()
    try:
        #add
        name = "Maciej"
        surname = "Tomaszewski"
        pesel = "14205914328"
        subject_name = "Test3"
        status = "absent"
        date = datetime(2025, 11, 11)

        studentID = StudentRepository.add_student_inside_another_transaction(session, name, surname, pesel)
        subjectID = SubjectRepository.add_subject_inside_another_transaction(session, subject_name)
        attendanceID = AttendanceRepository.add_attendance_inside_another_transaction(session, student_id=studentID, subject_id=subjectID, status=status, date=date)
        attendance = AttendanceRepository.get_attendance_inside_another_transaction(session, attendanceID)

        assert attendance is not None
        assert attendance.status == status
        assert attendance.date == date

        #edit
        status = "late"
        AttendanceRepository.edit_attendance_inside_another_transaction(session, attendance_id=attendanceID, status=status)
        attendance = AttendanceRepository.get_attendance_inside_another_transaction(session, attendance)

        assert attendance is not None
        assert attendance.status == status

        StudentRepository.delete_student_inside_another_transaction(session, studentID)
        SubjectRepository.delete_subject_inside_another_transaction(session, subjectID)
        AttendanceRepository.delete_subject_inside_another_tranasction(session, attendanceID)

        with pytest.raises(NoResultFound):
            StudentRepository.get_student_inside_another_transaction(session, studentID)
            SubjectRepository.get_subject_inside_another_transaction(session, subjectID)
            AttendanceRepository.get_attendance_inside_another_transaction(session, attendanceID)
    finally:
        session.rollback()
        session.close()




