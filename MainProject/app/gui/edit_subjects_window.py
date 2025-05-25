from customtkinter import *
from tkinter import messagebox
from psycopg2 import IntegrityError
from MainProject.app.services.subject_service import SubjectService
from MainProject.app.gui.tool_tip import ToolTip

class EditSubjectsWindow(CTkToplevel):
    def __init__(self, parent, session):
        super().__init__(parent)
        self.session = session
        self.title("Edit Subjects")
        self.transient(parent)
        self.grab_set()  # blokuje interakcję z innymi oknami aż to okno zostanie zamknięte
        self.focus()
        self.geometry("500x400")
        self.iconbitmap("gui/icons/editor.ico")
        self.resizable(False, False)

        self.selected_subject = IntVar(value=0)

        self.label = CTkLabel(self, text="Choose subject:")
        self.label.place(x=200, y=10)

        self.scrollable_frame = CTkScrollableFrame(self, width=400, height=100)
        self.scrollable_frame.place(x=50, y=40)

        self.new_name_label = CTkLabel(self, text="Subject name*")
        self.new_name_label.place(x=100, y=270)
        ToolTip(self.new_name_label, "Enter name to be modified or added")

        self.name_entry = CTkEntry(self, width=200)
        self.name_entry.place(x=200, y=270)

        self.rename_button = CTkButton(self, text="Change name", command=self.rename_subject, width=100, height=40, fg_color="#fc9803", hover_color="#a16103", text_color="black")
        self.rename_button.place(x=200, y=340)

        self.delete_button = CTkButton(self, text="Delete", command=self.delete_subject, width=100, height=40, fg_color="#96230f", hover_color="#541004", text_color="black")
        self.delete_button.place(x=325, y=340)

        self.add_button = CTkButton(self, text="Add subject", command=self.add_subject, width=100, height=40, fg_color="#11ad1e", hover_color="#0a5710", text_color="black")
        self.add_button.place(x=75, y=340)

        self.refresh_subjects()

    def refresh_subjects(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        subjects = SubjectService.get_all_subjects(self.session)
        for subj in subjects:
            CTkRadioButton(
                self.scrollable_frame,
                text=subj.name,
                variable=self.selected_subject,
                value=subj.id
            ).pack(anchor="w", pady=5, padx=5)

        self.selected_subject.set(0)

    def rename_subject(self):
        selected_id = self.selected_subject.get()
        new_name = self.name_entry.get().strip()
        if not selected_id:
            messagebox.showwarning("Error", "Choose the subject ")
            return
        if not new_name:
            messagebox.showwarning("Error", "Enter new name")
            return
        try:
            SubjectService.edit_subject(self.session, int(selected_id), new_name)
            self.session.commit()
            messagebox.showinfo("Success", f"Name changed to  '{new_name}'")
            self.refresh_subjects()
            self.name_entry.delete(0, END)
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", str(e))

    def delete_subject(self):
        selected = self.selected_subject.get()
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
            subject = SubjectService.get_subject(session=self.session, subject_id=selected)
            subject_name = subject.name

            SubjectService.delete_subject_name(self.session, selected)
            self.session.commit()

            messagebox.showinfo("Success", f"Deleted subject '{subject_name}'")
            self.refresh_subjects()
            self.selected_subject.set(0)

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", str(e))

    def add_subject(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Error", "Enter subject name")
            return
        try:
            SubjectService.add_subject(self.session, name)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            messagebox.showerror("Error", f"Subject '{name}' already exists.")
            return
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", str({e}))
            return

        messagebox.showinfo("Success", f"Subject '{name}' added succesfully")
        self.refresh_subjects()
