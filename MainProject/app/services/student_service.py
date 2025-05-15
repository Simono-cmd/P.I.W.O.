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
            return failure is not None #0 zdaje 1 zagrożony
        finally:
            session.close()

    @staticmethod
    def get_average_from_subject(student_id: int, subject_id: int) -> float:
        session = SessionLocal()
        try:
            grades = session.query(Grade).filter_by(student_id=student_id, subject_id=subject_id).all()
            if not grades:
                return 0.0
            total = sum(grade.value for grade in grades)
            average = total / len(grades)
            return round(average, 2)
        finally:
            session.close()

    @staticmethod
    def get_total_average(student_id: int) -> float:
        session = SessionLocal()
        try:
            grades = session.query(Grade).filter_by(student_id=student_id).all()
            if not grades:
                return 0.0  # brak ocen
            total = sum(grade.value for grade in grades)
            average = total / len(grades)
            return round(average, 2)
        finally:
            session.close()




















