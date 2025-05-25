from datetime import datetime
from MainProject.app.database.database import SessionLocal
from MainProject.app.models.attendance import Attendance
from sqlalchemy.exc import NoResultFound

class AttendanceRepository:

    @staticmethod
    def add_attendance(session: SessionLocal, student_id: int, subject_id: int, status: str, date_of: datetime) -> int:
        attendance = Attendance(student_id=student_id, subject_id=subject_id, status=status, date=date_of)
        session.add(attendance)
        session.flush()
        return attendance.id


    @staticmethod
    def edit_attendance(session: SessionLocal, attendance_id: int, student_id: int = None, subject_id: int = None, status: str = None,
                        date_of: datetime = None):
            attendance = session.query(Attendance).get(attendance_id)
            if attendance is None:
                raise NoResultFound("Attendance with id {} not found".format(attendance_id))

            if student_id: attendance.student_id = student_id
            if subject_id: attendance.subject_id = subject_id
            if status: attendance.status = status
            if date_of: attendance.date = date_of
            session.flush()


    @staticmethod
    def delete_attendance(session: SessionLocal, attendance_id: int):

        attendance = session.query(Attendance).get(attendance_id)
        if attendance is None:
            raise NoResultFound("Attendance with id {} not found".format(attendance_id))

        session.delete(attendance)
        session.flush()


    @staticmethod
    def get_attendance(session: SessionLocal, attendance_id: int):
        attendance = session.query(Attendance).get(attendance_id)
        if attendance is None:
            raise NoResultFound("Attendance with id {} not found".format(attendance_id))

        return attendance
