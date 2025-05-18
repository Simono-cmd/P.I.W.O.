
from datetime import datetime, date

from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.models.attendance import Attendance
from app.repositories.attendance_repository import AttendanceRepository


class AttendanceService:

    @staticmethod
    def add_attendance_inside_another_transaction(session: SessionLocal, student_id: int, subject_id: int, status: str, date_of: datetime) -> int:
        attendance_id = AttendanceRepository.add_attendance_inside_another_transaction(session, student_id, subject_id, status, date_of)
        return attendance_id

    @staticmethod
    def edit_attendance_inside_another_transaction(session: SessionLocal, attendance_id: int,
                                                   student_id: int = None, subject_id: int = None,
                                                   status: str = None,
                                                   date_of: datetime = None):
        AttendanceRepository.edit_attendance_inside_another_transaction(session, attendance_id, student_id, subject_id, status, date_of)

    @staticmethod
    def delete_attendance_inside_another_transaction(session: SessionLocal, attendance_id: int):
        AttendanceRepository.delete_attendance_inside_another_transaction(session, attendance_id)

    @staticmethod
    def get_attendance_inside_another_transaction(session: SessionLocal, attendance_id: int):
        attendance = AttendanceRepository.get_attendance_inside_another_transaction(session, attendance_id)
        return attendance


    @staticmethod
    def get_attendance_for_subject_on_date_inside_another_transaction(session: SessionLocal, subject_id: int, target_date: date):
        attendances = session.query(Attendance).filter(
            Attendance.subject_id == subject_id,
            Attendance.date == target_date
        ).options(joinedload(Attendance.student)).all()

        result = []
        for att in attendances:
            student_info = {
                "student_id": att.student_id,
                "student_name": att.student.name,
                "status": att.status
            }
            result.append(student_info)

        return result


