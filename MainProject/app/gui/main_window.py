from datetime import datetime
import tkinter as tk
from customtkinter import *
from tkinter import messagebox
from sqlalchemy.exc import IntegrityError
from MainProject.app.database.database import SessionLocal
from MainProject.app.gui.edit_attendances_window import EditAttendancesWindow
from MainProject.app.gui.edit_grades_window import EditGradesWindow
from MainProject.app.gui.edit_subjects_window import EditSubjectsWindow
from MainProject.app.gui.generate_reports_window import ReportWindow
from MainProject.app.gui.tool_tip import ToolTip
from MainProject.app.services.attendance_service import AttendanceService
from MainProject.app.services.failure_service import FailureService
from MainProject.app.services.student_service import StudentService
from MainProject.app.services.subject_service import SubjectService


class MainWindow(CTk):
    def __init__(self, session: SessionLocal):
        # conf
        super().__init__()
        self.sessionL = session
        set_appearance_mode("dark")
        set_default_color_theme("green")
        self.title("P.I.W.O.  v1.0")
        self.geometry("800x600")
        self.resizable(True, True)
        self.iconbitmap("gui/icons/icon.ico")

        # frames
        self.top_frame = CTkFrame(self, height=100)
        self.top_frame.pack(fill="x", pady=5, padx=10)

        self.bottom_frame = CTkFrame(self)
        self.bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_side_frame = CTkFrame(self.bottom_frame, fg_color="transparent")
        self.left_side_frame.pack(side="left", padx=20, fill="y", expand=True)

        self.right_side_frame = CTkFrame(self.bottom_frame, fg_color="transparent")
        self.right_side_frame.pack(side="right", padx=20, fill="y")

        self.list_frame = CTkFrame(self.left_side_frame, width=220, height=450, fg_color="#2b2b2b")
        self.list_frame.pack_propagate(False)
        self.list_frame.pack(side="top", fill="x")

        self.grades_and_attendance_frame = CTkFrame(self.left_side_frame, fg_color="#2b2b2b")
        self.grades_and_attendance_frame.pack(side="top", fill="y", anchor="n")

        self.list_frame_buttons = CTkFrame(self.bottom_frame, fg_color="#2b2b2b")
        self.list_frame_buttons.pack(side="top", anchor="w", padx=5, pady=50)

        self.report_buttons_frame = CTkFrame(self.right_side_frame, fg_color="#2b2b2b")
        self.report_buttons_frame.pack(side="bottom", pady=50)

        self.add_choose_subject_option()

    def add_choose_subject_option(self):
        subject = StringVar()
        subject_objects = SubjectService.get_all_subjects(self.sessionL)
        subject_names = [subject.name if hasattr(subject, "name") else subject for subject in subject_objects]

        subject_label = CTkLabel(self.top_frame, text="Choose a subject:", text_color="white")
        subject_label.grid(row=0, column=0, padx=5)

        subject_combo = CTkComboBox(self.top_frame,
                                    width=200,
                                    variable=subject,
                                    values=subject_names,
                                    command=lambda selected: self.add_students_list(selected))
        subject_combo.grid(row=0, column=1, padx=5)

        subject_combo.bind("<Key>", lambda e: "break")
        subject_combo.bind("<Button-3>", lambda e: "break")
        subject_combo.bind("<Control-v>", lambda e: "break")
        subject_combo.bind("<Shift-Insert>", lambda e: "break")

        edit_subject_button = CTkButton(
            self.top_frame,
            text="Edit subjects",fg_color="#cccccc", hover_color="#8d8d8d", text_color="black",
            command=lambda: self.open_subject_edit_window(subject_combo)
        )
        edit_subject_button.grid(row=0, column=2, padx=5)

    def add_students_list(self, subject: str):
        self.selected_subject = subject
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.selected_student = None
        self.students_labels = []

        self.students_enrolled = SubjectService.get_students_enrolled_in_subject(self.sessionL, subject)
        self.scroll_frame = CTkScrollableFrame(self.list_frame, fg_color="#242424")
        self.scroll_frame.pack(fill="both", expand=True, pady=50)

        for student in self.students_enrolled:
            full_name = f"{student.name} {student.surname}"
            label = CTkLabel(self.scroll_frame, text=full_name, text_color="white", anchor="w", fg_color="transparent")

            if FailureService.is_student_at_risk(self.sessionL, student.id,
                                                        SubjectService.find_subject_id_by_name(self.sessionL,
                                                                                               self.selected_subject)):
                label.configure(text_color="red")
            else:
                label.configure(text_color="white")

            label.pack(fill="x", pady=5)
            label.bind("<Button-1>",
                        lambda event, student_id=student.id, lbl=label: self.select_student(student_id, lbl))
            self.students_labels.append(label)

        self.add_buttons_to_list()
        self.add_grades_and_attendance_button()
        self.add_report_button()

    def add_buttons_to_list(self):
        for widget in self.list_frame_buttons.winfo_children():
            widget.destroy()

        self.form_frame = CTkFrame(self.list_frame_buttons, fg_color="transparent")
        self.form_frame.pack(side="top", pady=10)

        name_label = CTkLabel(self.form_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.name_entry = CTkEntry(self.form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        ToolTip(self.name_entry, "Enter student name to add or edit")

        surname_label = CTkLabel(self.form_frame, text="Surname:")
        surname_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.surname_entry = CTkEntry(self.form_frame)
        self.surname_entry.grid(row=1, column=1, padx=5, pady=2)
        ToolTip(self.surname_entry, "Enter student surname to add or edit")

        pesel_label = CTkLabel(self.form_frame, text="PESEL:")
        pesel_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.pesel_entry = CTkEntry(self.form_frame)
        self.pesel_entry.grid(row=2, column=1, padx=5, pady=2)
        ToolTip(self.pesel_entry, "Enter student PESEL to add or edit")

        add_button = CTkButton(self.list_frame_buttons, text="Add", command=self.add_student, fg_color="#3c971d", hover_color="#327a1a" )
        add_button.pack(side="top", pady=10)

        edit_button = CTkButton(self.list_frame_buttons, text="Edit", command=self.rename_student, fg_color="#fc8f0a", hover_color="#944309")
        edit_button.pack(side="top", pady=10)

        delete_button = CTkButton(self.list_frame_buttons, text="Delete",command=self.delete_student, fg_color="#b30415", hover_color="#57030c")
        delete_button.pack(side="top", pady=10)

    def select_student(self, student_id: int, label_widget: CTkLabel):
        for lbl in self.students_labels:
            lbl.configure(fg_color="transparent")

        self.selected_student = student_id
        label_widget.configure(fg_color="#3d91cf")

        student = StudentService.get_student(self.sessionL, student_id)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, student.name)

        self.surname_entry.delete(0, tk.END)
        self.surname_entry.insert(0, student.surname)

        self.pesel_entry.delete(0, tk.END)
        self.pesel_entry.insert(0, student.pesel)


    def add_grades_and_attendance_button(self):
        for widget in self.grades_and_attendance_frame.winfo_children():
            widget.destroy()

        grades_button = CTkButton(self.grades_and_attendance_frame, text="Grades", width=80, height=40, fg_color="#cccccc", hover_color="#8d8d8d", text_color="black", command=self.open_grade_edit_window)
        grades_button.pack(side="left", padx=(0, 10), fill="x", expand=True)

        attendance_button = CTkButton(self.grades_and_attendance_frame, text="Attendance", width=80, height=40, fg_color="#cccccc", hover_color="#8d8d8d", text_color="black", command=self.open_attendance_edit_window)
        attendance_button.pack(side="left", padx=(10, 0), fill="x", expand=True)

    def add_report_button(self):
        for widget in self.report_buttons_frame.winfo_children():
            widget.destroy()

        report_everyone_button = CTkButton(self.report_buttons_frame, text="Generate student's grade report", height=40, width=220, fg_color="#cccccc", hover_color="#8d8d8d", text_color="black", command=lambda: self.generate_grades_report_for_student(self.sessionL, self.selected_student))
        report_everyone_button.pack(pady=5, anchor="n")

        report_student_button = CTkButton(self.report_buttons_frame, text="Generate student's attendance report", height=40, width=220, fg_color="#cccccc", hover_color="#8d8d8d", text_color="black", command=lambda: self.generate_attendance_report_for_student(self.sessionL, self.selected_student))
        report_student_button.pack(pady=5, anchor="n")

        statistics_everyone_button = CTkButton(self.report_buttons_frame, text="Generate general statistics",  height=40, width=220, fg_color="#cccccc", hover_color="#8d8d8d", text_color="black", command=self.open_statistics_for_everyone)
        statistics_everyone_button.pack(pady=5, anchor="n")

        statistics_student_button = CTkButton(self.report_buttons_frame, text="Generate statistics for student", height=40, width=220, fg_color="#cccccc", hover_color="#8d8d8d", text_color="black", command= lambda: self.open_statistics_for_student(self.selected_student))
        statistics_student_button.pack(pady=5, anchor="n")

    def run(self):
        self.mainloop()
        self.sessionL.close()

    def open_subject_edit_window(self, subject_combo):
        edit_window = EditSubjectsWindow(self, self.sessionL)
        self.wait_window(edit_window)

        subject_objects = SubjectService.get_all_subjects(self.sessionL)
        subject_names = [subject.name for subject in subject_objects]

        subject_combo.configure(values=subject_names)

        if subject_names:
            subject_combo.set(subject_names[0])
            self.add_students_list(subject_names[0])


    def open_grade_edit_window(self):
        if not self.selected_student:
            messagebox.showwarning("Warning", "Please select a student from the list.")
            return
        edit_window = EditGradesWindow(self, self.sessionL, self.selected_student, self.selected_subject)
        self.wait_window(edit_window)
        self.refresh_students()


    def open_attendance_edit_window(self):
        if not self.selected_student:
            messagebox.showwarning("Warning", "Please select a student from the list.")
            return
        edit_window = EditAttendancesWindow(self, self.sessionL, self.selected_student, self.selected_subject)
        self.wait_window(edit_window)
        self.refresh_students()




    def rename_student(self):
        selected_id = self.selected_student
        new_name = self.name_entry.get().strip()
        new_surname = self.surname_entry.get().strip()
        new_pesel = self.pesel_entry.get().strip()
        if not selected_id:
            messagebox.showwarning("Error", "Choose the student")
            return
        if new_name=="" and new_pesel=="" and new_surname =="":
            messagebox.showwarning("Error", "Enter at least one new piece of information")
            return
        try:
            StudentService.edit_student(session=self.sessionL, student_id=selected_id, name=new_name, surname=new_surname, pesel=new_pesel)
            self.sessionL.commit()
            if new_name.strip() is not None and new_name.strip()!="": messagebox.showinfo("Success", f"Name changed to '{new_name}'")
            if new_surname.strip() is not None and new_surname.strip()!="": messagebox.showinfo("Success", f"Surname changed to '{new_surname}'")
            if new_pesel.strip() is not None and new_pesel.strip()!="": messagebox.showinfo("Success", f"PESEL changed to '{new_pesel}'")
            self.refresh_students()
            self.name_entry.delete(0, END)
        except Exception as e:
            self.sessionL.rollback()
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        selected = self.selected_student
        if not selected:
            messagebox.showwarning("Error", "Choose the student")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this student?\nAll attendances and grades will be deleted."
        )
        if not confirm:
            return

        try:
            student = StudentService.get_student(session=self.sessionL, student_id=selected)
            student_name = f"{student.name} {student.surname}"

            StudentService.delete_student(self.sessionL, selected)
            self.sessionL.commit()

            messagebox.showinfo("Success", f"Deleted student '{student_name}'")
            self.refresh_students()
            self.selected_student = None

        except Exception as e:
            self.sessionL.rollback()
            messagebox.showerror("Error", str(e))

    def add_student(self):
        imie = self.name_entry.get().strip()
        nazwisko = self.surname_entry.get().strip()
        pesel = self.pesel_entry.get().strip()

        if not imie:
            messagebox.showwarning("Nuh uh", "Enter student name")
            return
        if not nazwisko:
            messagebox.showwarning("Nuh uh", "Enter student surname")
            return
        if not pesel:
            messagebox.showwarning("Seriously?", "Enter student pesel")
            return
        try:
            if not StudentService.get_student_by_pesel(session=self.sessionL, pesel=pesel):
                StudentService.add_student(self.sessionL, name=imie, surname=nazwisko, pesel=pesel)
            new_student = StudentService.get_student_by_pesel(self.sessionL, pesel)
            AttendanceService.add_attendance(self.sessionL, student_id=new_student.id,
                                             subject_id=SubjectService.find_subject_id_by_name(self.sessionL,
                                                                                               self.selected_subject),
                                             status="present", date_of=datetime.now())
            self.sessionL.commit()
        except IntegrityError:
            self.sessionL.rollback()
            messagebox.showerror("Error", f"Student already exists.")
            return
        except Exception as e:
            self.sessionL.rollback()
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Success", f"Student '{imie} {nazwisko}' added succesfully")
        self.refresh_students()

    def refresh_students(self):
        self.add_students_list(self.selected_subject)

    def generate_grades_report_for_student(self, session: SessionLocal, student_id: int):
        if student_id is None:
            messagebox.showerror("Error", "Please select a student first.")
            return

        StudentService.generate_grades_report(session, student_id)
        messagebox.showinfo("Success", "Grades report generated succesfully. Check /Reports folder")

    def generate_attendance_report_for_student(self, session: SessionLocal, student_id: int):
        if student_id is None:
            messagebox.showerror("Error", "Please select a student first.")
            return

        StudentService.generate_attendance_report(session, student_id)
        messagebox.showinfo("Success", "Attendance report generated succesfully. Check /Reports folder")


    def open_statistics_for_student(self, student_id: int):
        if student_id is None:
            messagebox.showerror("Error", "Please select a student first.")
            return
        StudentService.generate_statistics_for_student(self.sessionL, student_id)
        report_window = ReportWindow(self, self.sessionL)

    def open_statistics_for_everyone(self):
        StudentService.generate_statistics_for_everyone(self.sessionL)
        report_window = ReportWindow(self, self.sessionL)