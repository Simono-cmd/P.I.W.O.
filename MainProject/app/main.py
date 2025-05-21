
from app.database.database import SessionLocal
from app.gui.main_window import MainWindow
from app.models import Grade
from app.services.grade_service import GradeService
from app.services.student_service import StudentService

session = SessionLocal()

try:
    # GradeService.add_grade(session=session, student_id=1, subject_id=1, form="test", worth=5)
    # GradeService.add_grade(session=session, student_id=1, subject_id=2, form="test", worth=2)
    # GradeService.add_grade(session=session, student_id=1, subject_id=2, form="test", worth=2)
    # GradeService.add_grade(session=session, student_id=1, subject_id=2, form="test", worth=2)
    # GradeService.add_grade(session=session, student_id=1, subject_id=1, form="short test", worth=4)

    StudentService.generate_statistics_for_student(session, 2)
    StudentService.generate_statistics_for_everyone(session)
    # StudentService.generate_grades_report(session, 1)
    # StudentService.generate_attendance_report(session, 1)
    session.close()
finally:
    session.rollback()
    session.close()
    if __name__ == "__main__":
        app = MainWindow()
        app.run()

# TODO
# 1. przycisk statystyk ma zwracac statystyki dla konkretnego przedmiotu, a nie dla kazdego przedmiotu
# 2. przycisku statystyk i reportu maja zwracac staty dla konkretnego studenta
# 3. dokonczyc grades i attendances buttony
# 4. ogarnac wyjatki
# 5. generowanie przykladowych danych