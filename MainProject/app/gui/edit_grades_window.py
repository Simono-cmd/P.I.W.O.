import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from MainProject.app.gui.tool_tip import ToolTip
from MainProject.app.services.grade_service import GradeService
from MainProject.app.models.grade import Grade
from MainProject.app.services.subject_service import SubjectService


class EditGradesWindow(CTkToplevel):
    def __init__(self, parent, session, student_id, subject_name):
        super().__init__(parent)
        self.session = session
        self.student_id = student_id
        self.subject_name = subject_name
        self.subject_id = SubjectService.find_subject_id_by_name(session, subject_name)
        self.selected_grade_id = None
        self.grab_set()
        self.focus()
        self.title("Edit grades")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap(os.path.abspath("gui/icons/editor.ico"))

        self.build_ui()
        self.load_grades()

    def build_ui(self):
        # Scrollable frame
        self.scrollable_frame = CTkScrollableFrame(self, height=250, width=150)
        self.scrollable_frame.pack(padx=10, pady=10)

        # Form and Worth inputs
        input_frame = CTkFrame(self)
        input_frame.pack(pady=10)

        self.form_entry = CTkEntry(input_frame, placeholder_text="Grade type")
        ToolTip(self.form_entry, text="Enter type [test/homework/short test]")
        self.form_entry.grid(row=0, column=0, padx=5)

        self.worth_entry = CTkEntry(input_frame, placeholder_text="Grade value")
        ToolTip(self.worth_entry, text="Enter value [1-6]")
        self.worth_entry.grid(row=0, column=1, padx=5)

        button_frame = CTkFrame(self)
        button_frame.pack(pady=10, padx=30)

        CTkButton(button_frame, text="Add", command=self.add_grade, width=80, fg_color="#3c971d", hover_color="#327a1a" ).grid(row=0, column=0, padx=5)
        CTkButton(button_frame, text="Edit", command=self.edit_selected_grade, width=80, fg_color="#fc8f0a", hover_color="#944309").grid(row=0, column=1, padx=5)
        CTkButton(button_frame, text="Delete", command=self.delete_selected_grade, width=80, fg_color="#b30415", hover_color="#57030c").grid(row=0, column=2,
                                                                                                 padx=5)

    def load_grades(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        grades = self.session.query(Grade).filter_by(student_id=self.student_id, subject_id=self.subject_id).all()
        self.grade_labels = {}

        for grade in grades:
            label_text = f"{grade.worth}  [{grade.form}]"
            label = CTkLabel(self.scrollable_frame, text=label_text, width=400, anchor="w", cursor="hand2")
            label.pack(pady=2, padx=5, anchor="w")
            label.bind("<Button-1>", lambda e, g_id=grade.id: self.select_grade(g_id))
            self.grade_labels[grade.id] = label

    def select_grade(self, grade_id):
        self.selected_grade_id = grade_id

        for g_id, label in self.grade_labels.items():
            if g_id == grade_id:
                label.configure(fg_color="#2e86de")
            else:
                label.configure(fg_color="transparent")

        grade = GradeService.get_grade(self.session, grade_id)
        self.form_entry.delete(0, tk.END)
        self.form_entry.insert(0, grade.form)
        self.worth_entry.delete(0, tk.END)
        self.worth_entry.insert(0, str(grade.worth))


    def add_grade(self):
        form = self.form_entry.get().strip()
        worth = self.worth_entry.get().strip()
        if not form or not worth.isdigit():
            messagebox.showerror("Error", "Invalid form or worth")
            return
        GradeService.add_grade(self.session, self.student_id, self.subject_id, form, int(worth))
        self.session.commit()
        self.load_grades()

    def edit_selected_grade(self):
        if not self.selected_grade_id:
            messagebox.showerror("Error", "No grade selected")
            return

        form = self.form_entry.get().strip()
        worth = self.worth_entry.get().strip()
        if not form or not worth.isdigit():
            messagebox.showerror("Error", "Invalid form or worth")
            return

        GradeService.edit_grade(self.session, self.selected_grade_id, form=form, worth=int(worth))
        self.session.commit()
        self.load_grades()

    def delete_selected_grade(self):
        if not self.selected_grade_id:
            messagebox.showerror("Error", "No grade selected")
            return

        GradeService.delete_grade(self.session, self.selected_grade_id)
        self.session.commit()
        self.selected_grade_id = None
        self.form_entry.delete(0, tk.END)
        self.worth_entry.delete(0, tk.END)
        self.load_grades()


