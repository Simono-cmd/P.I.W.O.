from app.database.database import SessionLocal
from app.models.attendance import Attendance
from app.models.failure import Failure
from app.models.grade import Grade


class StudentService:
    @staticmethod
    def get_student_attendances_from_subject(student_id: int, subject_id: int):
        session = SessionLocal()
        try:
            return session.query(Attendance).filter_by(
                student_id=student_id,
                subject_id=subject_id
            ).all()
        finally:
            session.close()

    @staticmethod
    def get_student_grades_from_subject(student_id: int, subject_id: int):
        session = SessionLocal()
        try:
            return session.query(Grade).filter_by(
                student_id=student_id,
                subject_id=subject_id
            ).all()
        finally:
            session.close()

    @staticmethod
    def is_student_at_risk(student_id: int, subject_id: int) -> bool:
        session = SessionLocal()
        try:
            failure = (session.query(Failure).filter_by(
                student_id=student_id,
                subject_id=subject_id)
                       .first())
            return failure is not None
        finally:
            session.close()




















