from sqlalchemy.exc import NoResultFound
from app.database.database import SessionLocal
from app.models.attendance import Attendance
from app.models.grade import Grade
from app.models.student import Student


class StudentRepository:

    #add student to table Students
    @staticmethod
    def add_student(name : str, surname : str, pesel : str) -> int:
        session = SessionLocal()
        try:
            student = Student(name=name, surname=surname, pesel=pesel)
            session.add(student)
            session.commit()
            return student.id
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


##################################################


    # add student to table Students
    @staticmethod
    def add_student_inside_another_transaction(session: SessionLocal, name: str, surname: str, pesel: str) -> int:
        student = Student(name=name, surname=surname, pesel=pesel)
        session.add(student)
        session.flush()
        return student.id


    @staticmethod
    def edit_student_inside_another_transaction(session: SessionLocal, student_id: int, name: str = None, surname: str = None, pesel: str = None):
            student = session.query(Student).get(student_id)
            if not student:
                raise NoResultFound(f"Student with id {student_id} not found")

            if name: student.name = name
            if surname: student.surname = surname
            if pesel: student.pesel = pesel
            session.flush()

    @staticmethod
    def delete_student_inside_another_transaction(session: SessionLocal, student_id: int):
        student = session.query(Student).get(student_id)
        if not student:
            raise NoResultFound(f"Student with id {student_id} not found")

        session.delete(student)
        session.flush()

    @staticmethod
    def get_student_inside_another_transaction(session: SessionLocal, student_id: int):
        student = session.query(Student).get(student_id)
        if not student:
            raise NoResultFound(f"Student with id {student_id} not found")
        session.flush()
        return student


















