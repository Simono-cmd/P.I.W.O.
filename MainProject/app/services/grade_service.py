from app.database.database import SessionLocal
from app.models.grade import Grade
from app.repositories.grade_repository import GradeRepository
from app.services.failure_service import FailureService


class GradeService:

    @staticmethod
    def add_grade(session: SessionLocal, student_id: int, subject_id: int, form: str,
                  worth: int) -> int:
        grade_id = GradeRepository.add_grade(session, student_id, subject_id, form.lower(), worth)
        FailureService.evaluate_student_risk(session, student_id, subject_id)
        return grade_id

    @staticmethod
    def edit_grade(session: SessionLocal, grade_id: int, student_id: int = None,
                   subject_id: int = None, form: str = None, worth: int = None):
        if form: form = form.lower()
        GradeRepository.edit_grade(session, grade_id, student_id, subject_id, form, worth)
        grade = GradeRepository.get_grade(session, grade_id)
        FailureService.evaluate_student_risk(session, grade.student_id, grade.subject_id)

    @staticmethod
    def delete_grade(session: SessionLocal, grade_id: int):
        grade = session.query(Grade).get(grade_id)
        FailureService.evaluate_student_risk(session, grade.student_id, grade.subject_id)
        GradeRepository.delete_grade(session, grade_id)

    @staticmethod
    def get_grade(session: SessionLocal, grade_id: int) -> Grade:
        return GradeRepository.get_grade(session, grade_id)