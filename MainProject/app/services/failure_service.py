from app.database.database import SessionLocal
from app.models.failure import Failure
from app.services.student_service import StudentService


class FailureService:

    @staticmethod
    def evaluate_student_risk(student_id: int, subject_id: int):
        session = SessionLocal()
        try:
            grades = StudentService.get_student_grades_from_subject(student_id, subject_id)
            attendances = StudentService.get_student_attendances_from_subject(student_id, subject_id)

            #calculate average
            if grades:
                avg_grade = sum([g.value for g in grades]) / len(grades)
            else:
                avg_grade = 0

            #calculate absences
            absences = [a for a in attendances if a.status == "absent"]
            num_absences = len(absences)

            #calculate late
            latenesses = [a for a in attendances if a.status == "late"]
            num_lates = len(latenesses)

            #total attendances
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

            session.commit()

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()