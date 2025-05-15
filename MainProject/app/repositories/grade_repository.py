from app.database.database import SessionLocal
from app.models.grade import Grade
from sqlalchemy.exc import NoResultFound

class GradeRepository:

    @staticmethod
    def add_grade(student_id: int, subject_id: int, form: str, worth: int) -> Grade:
        session = SessionLocal()
        try:
            grade = Grade(student_id=student_id, subject_id=subject_id, form=form, worth=worth)
            session.add(grade)
            session.commit()
            return grade
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def edit_grade(grade_id: int, student_id: int = None, subject_id: int = None, form: str = None, worth: int = None) -> Grade:
        session = SessionLocal()
        try:
            grade = session.query(Grade).get(grade_id)
            if grade is None:
                raise NoResultFound("Grade with id {} not found".format(grade_id))

            if student_id: grade.student_id = student_id
            if subject_id: grade.subject_id = subject_id
            if form: grade.form = form
            if worth: grade.worth = worth
            session.commit()
            return grade
        except NoResultFound:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete_grade(grade_id: int):
        session = SessionLocal()
        try:
            grade = session.query(Grade).get(grade_id)
            if grade is None:
                raise NoResultFound("Grade with id {} not found".format(grade_id))

            session.delete(grade)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_grade(grade_id: int) -> Grade:
        session = SessionLocal()
        try:
            grade = session.query(Grade).get(grade_id)
            if grade is None:
                raise NoResultFound("Grade with id {} not found".format(grade_id))

            return grade
        finally:
            session.close()