from datetime import datetime, date
from sqlalchemy.orm import joinedload
from MainProject.app.database.database import SessionLocal
from MainProject.app.models.attendance import Attendance
from MainProject.app.repositories.attendance_repository import AttendanceRepository
from MainProject.app.services.failure_service import FailureService


class AttendanceService:

    @staticmethod
    def add_attendance(session: SessionLocal, student_id: int, subject_id: int, status: str, date_of: datetime) -> int:
        attendance_id = AttendanceRepository.add_attendance(session, student_id, subject_id, status.lower(), date_of)
        FailureService.evaluate_student_risk(session, student_id, subject_id)
        return attendance_id

    @staticmethod
    def edit_attendance(session: SessionLocal, attendance_id: int,
                        student_id: int = None, subject_id: int = None,
                        status: str = None,
                        date_of: datetime = None):
        if status: status = status.lower()
        AttendanceRepository.edit_attendance(session, attendance_id, student_id, subject_id, status, date_of)

    @staticmethod
    def delete_attendance(session: SessionLocal, attendance_id: int):
        attendance = AttendanceRepository.get_attendance(session, attendance_id)
        AttendanceRepository.delete_attendance(session, attendance_id)
        FailureService.evaluate_student_risk(session, attendance.student_id, attendance.subject_id)

    @staticmethod
    def get_attendance(session: SessionLocal, attendance_id: int):
        attendance = AttendanceRepository.get_attendance(session, attendance_id)
        return attendance


    @staticmethod
    def get_attendance_for_subject_on_date(session: SessionLocal, subject_id: int, target_date: date):
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


