from app.database.database import SessionLocal
from app.models.grade import Grade
from app.repositories.grade_repository import GradeRepository
from app.services.failure_service import FailureService


class GradeService:

    @staticmethod
    def add_grade_inside_another_transaction(session: SessionLocal, student_id: int, subject_id: int, form: str,
                                             worth: int) -> int:
        grade_id = GradeRepository.add_grade_inside_another_transaction(session, student_id, subject_id, form, worth)
        FailureService.evaluate_student_risk_inside_another_transaction(session, student_id, subject_id)
        return grade_id

    @staticmethod
    def edit_grade_inside_another_transaction(session: SessionLocal, grade_id: int, student_id: int = None,
                                              subject_id: int = None, form: str = None, worth: int = None):
        GradeRepository.edit_grade_inside_another_transaction(session, grade_id, student_id, subject_id, form, worth)
        grade = GradeRepository.get_grade_inside_another_transaction(session, grade_id)
        FailureService.evaluate_student_risk_inside_another_transaction(session, grade.student_id, grade.subject_id)

    @staticmethod
    def delete_grade_inside_another_transaction(session: SessionLocal, grade_id: int):
        grade = session.query(Grade).get(grade_id)
        FailureService.evaluate_student_risk_inside_another_transaction(session, grade.student_id, grade.subject_id)
        GradeRepository.delete_grade_inside_another_transaction(session, grade_id)

    @staticmethod
    def get_grade_inside_another_transaction(session: SessionLocal, grade_id: int) -> Grade:
        return GradeRepository.get_grade_inside_another_transaction(session, grade_id)