import os
from pathlib import Path
from openpyxl.styles import Font, PatternFill
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from app.database.database import SessionLocal
from app.models import Subject, Student
from app.models.attendance import Attendance
from app.models.failure import Failure
from app.models.grade import Grade
from app.repositories.student_repository import StudentRepository
import openpyxl
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt


class StudentService:

    @staticmethod
    def add_student(session: SessionLocal, name: str, surname: str, pesel: str) -> int:
        return StudentRepository.add_student(session, name, surname, pesel)

    @staticmethod
    def edit_student(session: SessionLocal, student_id: int, name: str = None,
                     surname: str = None, pesel: str = None):
        StudentRepository.edit_student(session, student_id, name, surname, pesel)

    @staticmethod
    def delete_student(session: SessionLocal, student_id: int):
        StudentRepository.delete_student(session, student_id)

    @staticmethod
    def get_student(session: SessionLocal, student_id: int):
        return StudentRepository.get_student(session, student_id)

    @staticmethod
    def get_student_attendances_from_subject(session: SessionLocal, student_id: int, subject_id: int):
        return session.query(Attendance).filter_by(
            student_id=student_id,
            subject_id=subject_id
        ).all()


    @staticmethod
    def get_student_grades_from_subject(session: SessionLocal, student_id: int, subject_id: int):
        return session.query(Grade).filter_by(
            student_id=student_id,
            subject_id=subject_id
        ).all()

    @staticmethod
    def is_student_at_risk(session: SessionLocal, student_id: int, subject_id: int) -> bool:
        failure = (session.query(Failure).filter_by(
            student_id=student_id,
            subject_id=subject_id)
                   .first())
        return failure is not None #0 zdaje 1 zagrożony


    @staticmethod
    def get_average_from_subject(session: SessionLocal, student_id: int, subject_id: int) -> float:
        grades = session.query(Grade).filter_by(student_id=student_id, subject_id=subject_id).all()
        if not grades:
            return 0.0
        total = sum(grade.worth for grade in grades)
        average = total / len(grades)
        return round(average, 2)

    @staticmethod
    def get_total_average(session: SessionLocal, student_id: int) -> float:
        grades = session.query(Grade).filter_by(student_id=student_id).all()
        if not grades:
            return 0.0  # brak ocen
        total = sum(grade.worth for grade in grades)
        average = total / len(grades)
        return round(average, 2)

    @staticmethod
    def generate_grades_report(session: SessionLocal, student_id: int):
        student = StudentService.get_student(session, student_id)
        filename = "Grades.xlsx"
        documents_path = Path.home() / "Documents"
        reports_folder = documents_path / "Reports"
        student_folder = reports_folder / f"Student_{student_id}_{student.name}_{student.surname}"
        reports_folder.mkdir(parents=True, exist_ok=True)
        student_folder.mkdir(parents=True, exist_ok=True)
        full_path = reports_folder / student_folder / filename

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Grade report student {student_id}"

        light_blue_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")

        labels = ["Subject", "Average", "Grades"]
        for i, label in enumerate(labels, start=1):
            ws.cell(row=i, column=1, value=label).font = Font(bold=True, size=15, color="132A58")
        cell = ws.cell(row=1, column=1)
        cell.fill = light_blue_fill

        #pobierz jakoś przedmioty
        subjects = (session.query(Subject)
                    .join(Attendance, Attendance.subject_id == Subject.id)
                    .filter(Attendance.student_id == student_id)
                    .distinct()
                    .all())

        if not subjects:
            raise NoResultFound("Uczeń nie ma obecności na żadnym przedmiocie")

        for col, subject in enumerate(subjects, start=2):
            grades = StudentService.get_student_grades_from_subject(session, student_id, subject.id)
            average = StudentService.get_average_from_subject(session, student_id, subject.id)
            if StudentService.is_student_at_risk(session, student_id, subject.id):
                ws.cell(row=1, column=col, value=subject.name).font = Font(bold=True, size=11, color="FF0000")
                ws.cell(row=2, column=col, value=average).font = Font(size=11, color="FF0000")
            else:
                ws.cell(row=1, column=col, value=subject.name).font = Font(bold=True, size=11)
                ws.cell(row=2, column=col, value=average).font = Font(size=11, color="0089FF")
            cell = ws.cell(row=1, column=col)
            cell.fill = light_blue_fill
            for index, grade in enumerate(grades):
                ws.cell(row=3+index, column=col, value=grade.worth).font = Font(size=11)

        for col in ws.columns:
            col_letter = col[0].column_letter
            ws.column_dimensions[col_letter].width = 17

        for row in ws.iter_rows():
            row_index = row[0].row
            ws.row_dimensions[row_index].height = 17



        subject_cells = ws[1][1:]
        subjects = [cell.value for cell in subject_cells]

        value_cells = ws[2][1:]
        values = [cell.value for cell in value_cells]

        plt.figure(figsize=(6, 4))
        bars = plt.bar(subjects, values, color='skyblue')
        plt.title("Average per subject")
        plt.ylabel("Average")
        plt.ylim(0, 5)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom')

        img_path = student_folder / "avg_per_subject.png"
        plt.savefig(img_path)
        plt.close()

        img = Image(img_path)
        ws.add_image(img, "B9")

        wb.save(str(full_path))
        os.remove(img_path)


    @staticmethod
    def generate_attendance_report(session: SessionLocal, student_id: int):

        student = StudentService.get_student(session, student_id)
        filename = "Attendances.xlsx"
        documents_path = Path.home() / "Documents"
        reports_folder = documents_path / "Reports"
        student_folder = reports_folder / f"Student_{student_id}_{student.name}_{student.surname}"
        reports_folder.mkdir(parents=True, exist_ok=True)
        student_folder.mkdir(parents=True, exist_ok=True)
        full_path = reports_folder / student_folder / filename

        light_blue_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Attendance report student {student_id}"
        labels = Attendance.possible_status_values

        for i, label in enumerate(labels, start=1):
            ws.cell(row=i, column=1, value=label).font = Font(bold=True, size=15, color="132A58")
        cell = ws.cell(row=1, column=1)
        cell.fill = light_blue_fill
        attendances = (session.query(Attendance).filter(Attendance.student_id == student_id).all())
        subjects = (session.query(Subject).join(Attendance, Attendance.subject_id == Subject.id).filter(Attendance.student_id == student_id).distinct().all())

        for col, subject in enumerate(subjects, start = 2):
            ws.cell(row=1, column=col, value = subject.name).font = Font(bold = True, size = 11)
            for i, label in enumerate(labels[1:]):
                attendance_count = sum(1 for attendance in attendances if attendance.status.lower() == label.lower() and attendance.subject_id == subject.id)
                ws.cell(row=2 + i, column=col, value=attendance_count).font = Font(bold=True, size=11)

        for col in ws.columns:
            col_letter = col[0].column_letter
            ws.column_dimensions[col_letter].width = 17

        for row in ws.iter_rows():
            row_index = row[0].row
            ws.row_dimensions[row_index].height = 17

        wb.save(str(full_path))


    @staticmethod
    def generate_statistics_for_student(session: SessionLocal, student_id: int):
        student = StudentService.get_student(session, student_id)
        filename = "Statistics.xlsx"
        documents_path = Path.home() / "Documents"
        statistics_folder = documents_path / "Statistics"
        student_folder = statistics_folder / f"Student_{student_id}_{student.name}_{student.surname}"
        statistics_folder.mkdir(parents=True, exist_ok=True)
        student_folder.mkdir(parents=True, exist_ok=True)
        full_path = statistics_folder / student_folder / filename

        # calculate average grade value for each subject
        grades = session.query(Subject.name, func.avg(Grade.worth)).select_from(Grade).join(Subject, Subject.id == Grade.subject_id).join(Student, Student.id == Grade.student_id).filter(Grade.student_id == student_id).group_by(Subject.name).all()
        print(grades)

        # calculate average attendences per subject
        subject_count = session.query(func.count(func.distinct(Attendance.subject_id))).filter(Attendance.student_id == student_id).scalar()
        if subject_count != 0:
            attendences = session.query(Attendance.status, func.count(Attendance.status) / subject_count).filter(Attendance.student_id == student_id).group_by(Attendance.status).all()
        else :
            attendences = []
        print(attendences)
        print(subject_count)

        # calculate percentage of how many subjects are being failed
        if subject_count != 0:
            failure_percentage = session.query(func.count(Failure.student_id)).filter(Failure.student_id == student_id).scalar() / subject_count * 100
        else:
            failure_percentage = 0
        print(failure_percentage)


    @staticmethod
    def generate_statistics_for_everyone(session: SessionLocal):
        filename = "Statistics.xlsx"
        documents_path = Path.home() / "Documents"
        statistics_folder = documents_path / "Statistics"
        statistics_folder.mkdir(parents=True, exist_ok=True)
        full_path = statistics_folder / filename

        # calculate average grade value for each subject
        grades = session.query(Subject.name, func.avg(Grade.worth)).select_from(Grade).join(Subject, Subject.id == Grade.subject_id).group_by(Subject.name).all()
        print(grades)

        # calculate average attendences
        student_count = session.query(func.count(Student.id)).scalar()
        attendences = session.query(Attendance.status, func.count(Attendance.status) / student_count).group_by(Attendance.status).all()
        print(attendences)

        # calculate percentage of people failing
        failure_percentage = session.query(func.count(Failure.student_id)).distinct().scalar() / student_count * 100
        print(failure_percentage)



