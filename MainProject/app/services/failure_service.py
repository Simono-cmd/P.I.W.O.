from MainProject.app.database.database import SessionLocal
from MainProject.app.models.failure import Failure
from MainProject.app.services.student_service import StudentService


class FailureService:


    @staticmethod
    def evaluate_student_risk(session: SessionLocal, student_id: int, subject_id: int) -> None:
        grades = StudentService.get_student_grades_from_subject(session, student_id, subject_id)
        attendances = StudentService.get_student_attendances_from_subject(session, student_id, subject_id)

        # calculate average
        if grades:
            avg_grade = sum([g.worth for g in grades]) / len(grades)
        else:
            avg_grade = 0.0

        # calculate absences
        absences = [a for a in attendances if a.status.lower() == "absent"]
        num_absences = len(absences)

        # calculate late
        latenesses = [a for a in attendances if a.status.lower() == "late"]
        num_lates = len(latenesses)

        # total attendances
        total_classes = len(attendances)

        is_at_risk = (
                avg_grade < 3 or
                num_absences > 2 or
                (total_classes > 0 and num_lates >= total_classes / 2)
        )

        existing = session.query(Failure).filter_by(student_id=student_id, subject_id=subject_id).first()

        if is_at_risk:
            if not existing:
                failure = Failure(student_id=student_id, subject_id=subject_id)
                session.add(failure)
        else:
            if existing:
                session.delete(existing)

        session.flush()

    @staticmethod
    def is_student_at_risk(session: SessionLocal, student_id: int, subject_id: int) -> bool:
        failure = session.query(Failure).filter_by(student_id=student_id, subject_id=subject_id).first()
        return failure is not None



