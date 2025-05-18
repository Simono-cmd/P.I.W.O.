from app.database.database import SessionLocal
from app.models.attendance import Attendance
from app.models.failure import Failure
from app.models.grade import Grade
from app.repositories.student_repository import StudentRepository


class StudentService:

    @staticmethod
    def add_student_inside_another_transaction(session: SessionLocal, name: str, surname: str, pesel: str) -> int:
        return StudentRepository.add_student_inside_another_transaction(session, name, surname, pesel)

    @staticmethod
    def edit_student_inside_another_transaction(session: SessionLocal, student_id: int, name: str = None,
                                                surname: str = None, pesel: str = None):
        StudentRepository.edit_student_inside_another_transaction(session, student_id, name, surname, pesel)

    @staticmethod
    def delete_student_inside_another_transaction(session: SessionLocal, student_id: int):
        StudentRepository.delete_student_inside_another_transaction(session, student_id)

    @staticmethod
    def get_student_inside_another_transaction(session: SessionLocal, student_id: int):
        return StudentRepository.get_student_inside_another_transaction(session, student_id)

    @staticmethod
    def get_student_attendances_from_subject_inside_another_transaction(session: SessionLocal, student_id: int, subject_id: int):
        return session.query(Attendance).filter_by(
            student_id=student_id,
            subject_id=subject_id
        ).all()


    @staticmethod
    def get_student_grades_from_subject_inside_another_transaction(session: SessionLocal, student_id: int, subject_id: int):
        return session.query(Grade).filter_by(
            student_id=student_id,
            subject_id=subject_id
        ).all()

    @staticmethod
    def is_student_at_risk_inside_another_transaction(session: SessionLocal, student_id: int, subject_id: int) -> bool:
        failure = (session.query(Failure).filter_by(
            student_id=student_id,
            subject_id=subject_id)
                   .first())
        return failure is not None #0 zdaje 1 zagrożony


    @staticmethod
    def get_average_from_subject_inside_another_transaction(session: SessionLocal, student_id: int, subject_id: int) -> float:
        grades = session.query(Grade).filter_by(student_id=student_id, subject_id=subject_id).all()
        if not grades:
            return 0.0
        total = sum(grade.value for grade in grades)
        average = total / len(grades)
        return round(average, 2)

    @staticmethod
    def get_total_average_inside_another_transaction(session: SessionLocal, student_id: int) -> float:
        grades = session.query(Grade).filter_by(student_id=student_id).all()
        if not grades:
            return 0.0  # brak ocen
        total = sum(grade.value for grade in grades)
        average = total / len(grades)
        return round(average, 2)





















