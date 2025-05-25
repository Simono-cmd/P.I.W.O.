from sqlalchemy.exc import NoResultFound
from MainProject.app.database.database import SessionLocal
from MainProject.app.models.student import Student


class StudentRepository:


    # add student to table Students
    @staticmethod
    def add_student(session: SessionLocal, name: str, surname: str, pesel: str ) -> int:
        student = Student(name=name, surname=surname, pesel=pesel)
        session.add(student)
        session.flush()
        return student.id


    @staticmethod
    def edit_student(session: SessionLocal, student_id: int, name: str = None, surname: str = None, pesel: str = None):
            student = session.query(Student).get(student_id)
            if not student:
                raise NoResultFound(f"Student with id {student_id} not found")

            if name: student.name = name
            if surname: student.surname = surname
            if pesel: student.pesel = pesel
            session.flush()

    @staticmethod
    def delete_student(session: SessionLocal, student_id: int):
        student = session.query(Student).get(student_id)
        if not student:
            raise NoResultFound(f"Student with id {student_id} not found")

        session.delete(student)
        session.flush()

    @staticmethod
    def get_student(session: SessionLocal, student_id: int):
        student = session.query(Student).get(student_id)
        if not student:
            raise NoResultFound(f"Student with id {student_id} not found")
        return student

















