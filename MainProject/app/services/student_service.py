from sqlalchemy.exc import NoResultFound
from app.database.database import SessionLocal
from app.models.attendance import Attendance
from app.models.failure import Failure
from app.models.grade import Grade
from app.models.student import Student


class StudentService:

    #add student to table Students
    @staticmethod
    def add_student(name : str, surname : str, pesel : str):
        session = SessionLocal()
        try:
            student = Student(name=name, surname=surname, pesel=pesel)
            session.add(student)
            session.commit()
            return student
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def edit_student(student_id : int, name: str = None, surname: str = None, pesel: str = None):
        session = SessionLocal()
        try:
            student = session.query(Student).get(student_id)
            if not student:
                raise NoResultFound(f"Student with id {student_id} not found")
            if name: student.name = name
            if surname: student.surname = surname
            if pesel: student.pesel = pesel
            session.commit()
            session.refresh(student)
            return student
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_student(student_id: int):
        session = SessionLocal()
        try:
            student = session.query(Student).get(student_id)
            if not student:
                raise NoResultFound(f"Student with id {student_id} not found")
            session.delete(student)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_student(student_id: int):
        session = SessionLocal()
        try:
            student = session.query(Student).get(student_id)
            if not student:
                raise NoResultFound(f"Student with id {student_id} not found")
            return student
        finally:
            session.close()

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




















