import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import IntegrityError

from app.database.database import SessionLocal
from app.services.subject_service import SubjectService


class MainWindow():
    def __init__(self):
        self.sessionL = SessionLocal()
        self.root = tk.Tk()
        self.root.title("P.I.W.O alpha v1.0")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        img = tk.PhotoImage(file="gui/icon.png")
        self.root.iconphoto(False, img)
        self.root.configure(bg="black")

        self.subject = tk.StringVar()

        self.subject_label = tk.Label(self.root, text="Wybierz przedmiot: ")
        self.subject_combo = ttk.Combobox(self.root, width=20, textvariable=self.subject,
                                          values=SubjectService.get_all_subjects(self.sessionL))

        self.add_subject_box_label = tk.Label(self.root, text="Add subject (enter name): ")
        self.add_subject_box = tk.Text(self.root, width=60, height=5)

        self.add_subject_button = ttk.Button(self.root, text="Add", command=self.add_subject_and_commit)

        # Układ widgetów
        self.subject_label.place(x=10, y=10)
        self.subject_combo.place(x=150, y=10)
        self.add_subject_box_label.place(x=10, y=50)
        self.add_subject_box.place(x=10, y=80, width=300, height=100)
        self.add_subject_button.place(x=10, y=190)

    def add_subject_and_commit(self):
        name = self.add_subject_box.get("1.0", tk.END).strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a subject name.")
            return
        try:
            SubjectService.add_subject(session=self.sessionL, name=name)
            self.sessionL.commit()
        except IntegrityError:
            self.sessionL.rollback()
            messagebox.showerror("Error", f"Subject '{name}' already exists.")
            return
        except Exception as e:
            self.sessionL.rollback()
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            return

        # Odśwież combobox
        self.subject_combo['values'] = SubjectService.get_all_subjects(self.sessionL)
        self.add_subject_box.delete("1.0", tk.END)
        messagebox.showinfo("Success", f"Subject '{name}' added successfully.")

    def run(self):
        self.root.mainloop()
        self.sessionL.close()
