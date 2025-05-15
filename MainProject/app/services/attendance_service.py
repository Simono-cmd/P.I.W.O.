
from datetime import datetime, date

from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.models.attendance import Attendance
from sqlalchemy.exc import NoResultFound

class AttendanceService:
    from datetime import date
    from app.database.database import SessionLocal
    from app.models.attendance import Attendance
    from sqlalchemy.orm import joinedload

    class AttendanceService:
        @staticmethod
        def get_attendance_for_subject_on_date(subject_id: int, target_date: date):
            session = SessionLocal()
            try:
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
            finally:
                session.close()

