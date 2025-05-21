# app/gui/edit_attendances_window.py
from customtkinter import *

class EditAttendancesWindow(CTkToplevel):
    def __init__(self, parent, session, student_id, subject_name):
        super().__init__(parent)
        self.session = session
        self.title("Edit attendances")
        self.transient(parent)
        self.grab_set()
        self.focus()
        self.geometry("500x400")
        self.iconbitmap("gui/icons/editor.ico")
        self.resizable(False, False)
