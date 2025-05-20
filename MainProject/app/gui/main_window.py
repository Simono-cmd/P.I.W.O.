from datetime import datetime

from customtkinter import *
from tkinter import messagebox

from sqlalchemy import DateTime
from sqlalchemy.exc import IntegrityError
from app.database.database import SessionLocal
from app.gui.edit_subjects_window import EditSubjectsWindow
from app.gui.tool_tip import ToolTip
from app.services.attendance_service import AttendanceService
from app.services.student_service import StudentService
from app.services.subject_service import SubjectService


class MainWindow:
    def __init__(self):
        self.sessionL = SessionLocal()
        set_appearance_mode("dark")
        set_default_color_theme("green")
        self.root = CTk()
        self.root.title("P.I.W.O.  v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.iconbitmap("gui/icon.ico")

        #frames
        self.top_frame = CTkFrame(self.root)
        self.top_frame.pack(fill="x", pady=10, padx=10)
        self.bottom_frame = CTkFrame(self.root)
        self.bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.list_frame = CTkFrame(self.bottom_frame, width=200, height=400, fg_color="#2b2b2b")
        self.list_frame.pack_propagate(False)
        self.list_frame.pack(side="left", padx=40)
        self.list_frame_buttons = CTkFrame(self.bottom_frame, fg_color="#2b2b2b")
        self.list_frame_buttons.pack(side="left", padx=10)


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

        edit_subject_button = CTkButton(
            self.top_frame,
            text="Edit subjects",
            command=lambda: self.open_subject_edit_window(subject_combo)
        )
        edit_subject_button.grid(row=0, column=2, padx=5)

    def add_students_list(self, subject: str):
        self.selected_subject=subject
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.selected_student = None
        self.students_labels = [] #wybrany uczeń

        self.students_enrolled = SubjectService.get_students_enrolled_in_subject(self.sessionL, subject)
        self.scroll_frame = CTkScrollableFrame(self.list_frame, fg_color="#242424")
        self.scroll_frame.pack(fill="both", expand=True)

        for student in self.students_enrolled:
            full_name = f"{student.name} {student.surname}"

            label = CTkLabel(self.scroll_frame, text=full_name, text_color="white", anchor="w", fg_color="transparent")
            label.pack(fill="x", pady=5)
            label.bind("<Button-1>", lambda event, student_id=student.id, lbl=label: self.select_student(student_id, lbl))
        #button 1 left mouse click
            self.students_labels.append(label)

        self.add_buttons_to_list()

    def select_student(self, student_id: int, label_widget: CTkLabel):
        for lbl in self.students_labels:
            lbl.configure(fg_color="transparent")

        self.selected_student = student_id
        label_widget.configure(fg_color="#2fa572")

    def add_buttons_to_list(self):
        for widget in self.list_frame_buttons.winfo_children():
            widget.destroy()

        self.name_entry = CTkEntry(self.list_frame_buttons, width=140)
        ToolTip(self.name_entry, "Enter {name} {surname} {pesel} ")
        add_button = CTkButton(self.list_frame_buttons, text="Add", command=self.add_student)
        edit_button = CTkButton(self.list_frame_buttons, text="Edit", fg_color="#fc8f0a", hover_color="#944309")
        delete_button = CTkButton(self.list_frame_buttons, text="Delete", fg_color="#b30415", hover_color="#57030c")

        self.name_entry.pack(side="top", pady=10)
        add_button.pack(side="top", pady=10)
        edit_button.pack(side="top", pady=10)
        delete_button.pack(side="top", pady=10)


    def run(self):
        self.root.mainloop()
        self.sessionL.close()

    def open_subject_edit_window(self, subject_combo):
        edit_window = EditSubjectsWindow(self.root, self.sessionL)
        self.root.wait_window(edit_window)


        subject_objects = SubjectService.get_all_subjects(self.sessionL)
        subject_names = [subject.name for subject in subject_objects]

        subject_combo.configure(values=subject_names)

        if subject_names:
            subject_combo.set(subject_names[0])
            self.add_students_list(subject_names[0])

    def rename_student(self):
        selected_id = self.selected_student.get()
        new_name = self.name_entry.get().strip()
        if not selected_id:
            messagebox.showwarning("Error", "Choose the subject ")
            return
        if not new_name:
            messagebox.showwarning("Error", "Enter new name")
            return
        try:
            SubjectService.edit_subject(session=self.sessionL)
            self.sessionL.commit()
            messagebox.showinfo("Success", f"Name changed to  '{new_name}'")
            self.refresh_students()
            self.name_entry.delete(0, END)
        except Exception as e:
            self.sessionL.rollback()
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        selected = self.selected_student.get()
        if not selected:
            messagebox.showwarning("Error", "Choose the subject")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this subject?\nAll attendances and grades will be deleted."
        )
        if not confirm:
            return

        try:
            subject = SubjectService.get_subject(session=self.sessionL, subject_id=selected)
            subject_name = subject.name

            SubjectService.delete_subject_name(self.sessionL, selected)
            self.sessionL.commit()

            messagebox.showinfo("Success", f"Deleted subject '{subject_name}'")
            self.refresh_students()
            self.selected_student.set(0)

        except Exception as e:
            self.sessionL.rollback()
            messagebox.showerror("Error", str(e))

    def add_student(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Error", "Enter subject name")
            return
        try:
            parts = name.split(" ")
            if len(parts) != 3:
                messagebox.showwarning("Error", "Enter correct name and surname")
                return
            imie=parts[0]
            nazwisko=parts[1]
            pesel=parts[2]
            StudentService.add_student(self.sessionL, name=imie, surname=nazwisko, pesel=pesel)
            AttendanceService.add_attendance(self.sessionL, student_id=self.selected_student.get(), subject_id="", status="present", date_of=datetime.now())
            self.sessionL.commit()
        except IntegrityError:
            self.sessionL.rollback()
            messagebox.showerror("Error", f"Student already exists.")
            return
        except Exception as e:
            self.sessionL.rollback()
            messagebox.showerror("Error", str({e}))
            return

        messagebox.showinfo("Success", f"Subject '{name}' added succesfully")
        self.refresh_students()

    def refresh_students(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.students_enrolled = SubjectService.get_students_enrolled_in_subject(self.sessionL, subject)
        self.selected_student.set(0)

