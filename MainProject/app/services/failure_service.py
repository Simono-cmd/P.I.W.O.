from datetime import datetime
from app.database.database import SessionLocal
from app.models.attendance import Attendance
from sqlalchemy.exc import NoResultFound

# @staticmethod
# def evaluate_student_risk(student_id: int):
#     session = SessionLocal()
#     try:
#         student = session.query(Student).get(student_id)
#         if not student:
#             raise ValueError("Student not found")
#
#         #calculate absences
#         absences = session.query(Attendance).filter(
#             Attendance.student_id == student_id,
#             Attendance.status == "absent"
#         ).count()
#
#         #calculate being late
#         total_attendances = session.query(Attendance).filter(
#             Attendance.student_id == student_id
#         ).count()
#         late_attendances = session.query(Attendance).filter(
#             Attendance.student_id == student_id,
#             Attendance.status == "late"
#         ).count()
#
#         #calculate avg
#         grades = session.query(Grade.worth).filter(Grade.student_id == student_id).all()
#         total_grades = len(grades)
#         average = sum([g[0] for g in grades]) / total_grades if total_grades > 0 else 0
#
#         warnings = []
#
#         if absences > 2:
#             warnings.append("Więcej niż 2 nieobecności")
#
#         if total_attendances > 0 and late_attendances > (total_attendances / 2):
#             warnings.append("Spóźnienia na więcej niż połowę lekcji")
#
#         if average < 3:
#             warnings.append("Średnia ocen poniżej 3")
#
#         student.atRisk = len(warnings) > 0
#         session.commit()
#
#         return warnings
#
#     except Exception as e:
#         session.rollback()
#         raise e
#     finally:
#         session.close()