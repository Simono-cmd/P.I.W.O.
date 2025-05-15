from app.database.database import SessionLocal
from app.models.grade import Grade
from sqlalchemy.exc import NoResultFound
from app.services.failure_service import FailureService


class GradeRepository:

    @staticmethod
    def add_grade(student_id: int, subject_id: int, form: str, worth: int) -> int:
        session = SessionLocal()
        try:
            grade = Grade(student_id=student_id, subject_id=subject_id, form=form, worth=worth)
            session.add(grade)
            session.commit()
            FailureService.evaluate_student_risk(student_id, subject_id)
            return grade.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def edit_grade(grade_id: int, student_id: int = None, subject_id: int = None, form: str = None, worth: int = None) :
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
            FailureService.evaluate_student_risk(student_id, subject_id)
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
            student_id = grade.student_id
            subject_id = grade.subject_id
            session.delete(grade)
            session.commit()
            FailureService.evaluate_student_risk(student_id, subject_id)
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


#########################################



    @staticmethod
    def add_grade_inside_another_transaction(session: SessionLocal, student_id: int, subject_id: int, form: str, worth: int) -> int:
        grade = Grade(student_id=student_id, subject_id=subject_id, form=form, worth=worth)
        session.add(grade)
        session.flush()
        FailureService.evaluate_student_risk_inside_another_transaction(session, student_id, subject_id)
        return grade.id


    @staticmethod
    def edit_grade_inside_another_transaction(session: SessionLocal, grade_id: int, student_id: int = None, subject_id: int = None, form: str = None, worth: int = None) :
        grade = session.query(Grade).get(grade_id)
        if grade is None:
            raise NoResultFound("Grade with id {} not found".format(grade_id))

        if student_id: grade.student_id = student_id
        if subject_id: grade.subject_id = subject_id
        if form: grade.form = form
        if worth: grade.worth = worth
        session.flush()
        FailureService.evaluate_student_risk_inside_another_transaction(session, student_id, subject_id)


    @staticmethod
    def delete_grade_inside_another_transaction(session: SessionLocal, grade_id: int):
        grade = session.query(Grade).get(grade_id)
        if grade is None:
            raise NoResultFound("Grade with id {} not found".format(grade_id))
        student_id = grade.student_id
        subject_id = grade.subject_id
        session.delete(grade)
        session.flush()
        FailureService.evaluate_student_risk_inside_another_transaction(session, student_id, subject_id)


    @staticmethod
    def get_grade_inside_another_transaction(session: SessionLocal, grade_id: int) -> Grade:
            grade = session.query(Grade).get(grade_id)
            if grade is None:
                raise NoResultFound("Grade with id {} not found".format(grade_id))

            session.flush()
            return grade


###############################################################