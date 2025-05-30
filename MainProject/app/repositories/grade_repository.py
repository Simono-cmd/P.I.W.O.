from MainProject.app.database.database import SessionLocal
from MainProject.app.models.grade import Grade
from sqlalchemy.exc import NoResultFound


class GradeRepository:

    @staticmethod
    def add_grade(session: SessionLocal, student_id: int, subject_id: int, form: str, worth: int) -> int:
        grade = Grade(student_id=student_id, subject_id=subject_id, form=form, worth=worth)
        session.add(grade)
        session.flush()
        return grade.id


    @staticmethod
    def edit_grade(session: SessionLocal, grade_id: int, student_id: int = None, subject_id: int = None, form: str = None, worth: int = None) -> None:
        grade = session.query(Grade).get(grade_id)
        if grade is None:
            raise NoResultFound("Grade with id {} not found".format(grade_id))

        if student_id: grade.student_id = student_id
        if subject_id: grade.subject_id = subject_id
        if form: grade.form = form
        if worth: grade.worth = worth
        session.flush()


    @staticmethod
    def delete_grade(session: SessionLocal, grade_id: int) -> None:
        grade = session.query(Grade).get(grade_id)
        if grade is None:
            raise NoResultFound("Grade with id {} not found".format(grade_id))
        session.delete(grade)
        session.flush()


    @staticmethod
    def get_grade(session: SessionLocal, grade_id: int) -> Grade:
            grade = session.query(Grade).get(grade_id)
            if grade is None:
                raise NoResultFound("Grade with id {} not found".format(grade_id))
            return grade


