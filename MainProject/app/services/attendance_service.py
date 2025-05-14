from datetime import datetime

from app.database.database import SessionLocal
from app.models.attendance import Attendance
from sqlalchemy.exc import NoResultFound

class AttendanceService():

    @staticmethod
    def add_attendance(student_id: int, subject_id: int, status: str, date: datetime):
        session = SessionLocal()
        try:
            attendance = Attendance(student_id=student_id, subject_id=subject_id, status=status, date=date)
            session.add(attendance)
            session.commit()
            return attendance
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def edit_attendance(attendance_id: int, student_id: int = None, subject_id: int = None, status: str = None, date: datetime = None):
        session = SessionLocal()
        try:
            attendance = session.query(Attendance).get(attendance_id)
            if attendance is None:
                raise NoResultFound("Attendance with id {} not found".format(attendance_id))

            if student_id: attendance.student_id = student_id
            if subject_id: attendance.subject_id = subject_id
            if status: attendance.status = status
            if date: attendance.date = date
            session.commit()
            session.refresh()
            return attendance
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete_attendance(attendance_id: int):
        session = SessionLocal()
        try:
            attendance = session.query(Attendance).get(attendance_id)
            if attendance is None:
                raise NoResultFound("Attendance with id {} not found".format(attendance_id))

            session.delete(attendance)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_attendance(attendance_id: int):
        session = SessionLocal
        try:
            attendance = session.query(Attendance).get(attendance_id)
            if attendance is None:
                raise NoResultFound("Attendance with id {} not found".format(attendance_id))

            return attendance
        finally:
            session.close()


