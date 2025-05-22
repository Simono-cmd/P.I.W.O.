import calendar
import os
from datetime import datetime, date

import tkinter as tk
from tkinter import messagebox

from customtkinter import *

from app.services.attendance_service import AttendanceService
from app.services.subject_service import SubjectService
from app.models.attendance import Attendance


class EditAttendancesWindow(CTkToplevel):
    STATUS_COLORS = {
        "present": "#3cb043",
        "late": "#fca103",
        "excused": "#007fff",
        "absent": "#b30415"
    }

    MONTHS = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    def __init__(self, parent, session, student_id, subject_name):
        super().__init__(parent)
        self.session = session
        self.student_id = student_id
        self.subject_name = subject_name
        self.subject_id = SubjectService.find_subject_id_by_name(session, subject_name)

        self.title("Attendance Tracker")
        self.geometry("600x500")
        self.iconbitmap("gui/icons/editor.ico")
        self.grab_set()
        self.focus()
        self.resizable(False, False)

        self.selected_status = None
        self.selected_date = datetime.today().date()

        self.build_ui()
        self.draw_calendar()

    def build_ui(self):
        top_frame = CTkFrame(self)
        top_frame.pack(pady=10)

        self.year_var = tk.IntVar(value=self.selected_date.year)
        self.month_name_var = tk.StringVar(value=self.MONTHS[self.selected_date.month - 1])

        CTkLabel(top_frame, text="Year").grid(row=0, column=0, padx=5)
        self.year_entry = CTkEntry(top_frame, textvariable=self.year_var, width=70)
        self.year_entry.grid(row=0, column=1, padx=5)

        CTkLabel(top_frame, text="Month").grid(row=0, column=2, padx=5)
        self.month_menu = CTkOptionMenu(top_frame, values=self.MONTHS, variable=self.month_name_var)
        self.month_menu.grid(row=0, column=3, padx=5)

        CTkButton(top_frame, text=" 🡆 ", command=self.draw_calendar, width=40).grid(row=0, column=4, padx=10)

        self.calendar_frame = CTkFrame(self)
        self.calendar_frame.pack(pady=20)

        status_frame = CTkFrame(self)
        status_frame.pack(pady=10)

        self.status_buttons = {
            "present": CTkButton(status_frame, text="Present", fg_color="#3cb043", width=100,
                                 command=lambda: self.set_status("present")),
            "absent": CTkButton(status_frame, text="Absent", fg_color="#b30415", width=100,
                                command=lambda: self.set_status("absent")),
            "excused": CTkButton(status_frame, text="Excused", fg_color="#007fff",width=100,
                                 command=lambda: self.set_status("excused")),
            "late": CTkButton(status_frame, text="Late", fg_color="#fca103",width=100,
                              command=lambda: self.set_status("late")),
        }

        for i, btn in enumerate(self.status_buttons.values()):
            btn.grid(row=0, column=i, padx=10)

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        try:
            year = self.year_var.get()
            month_name = self.month_name_var.get()
            month = self.MONTHS.index(month_name) + 1

            cal = calendar.Calendar()
            days = cal.itermonthdays(year, month)

            for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
                CTkLabel(self.calendar_frame, text=day).grid(row=0, column=i, padx=5, pady=5)

            row = 1
            col = 0

            for day in days:
                if day == 0:
                    CTkLabel(self.calendar_frame, text="").grid(row=row, column=col, padx=5, pady=5)
                else:
                    this_date = date(year, month, day)
                    color = self.get_status_color(this_date)

                    btn = CTkButton(self.calendar_frame, text=str(day),fg_color=color or "gray20",command=lambda d=this_date: self.on_day_click(d),width=50, height=50)
                    btn.grid(row=row, column=col, padx=2, pady=2)

                col += 1
                if col > 6:
                    col = 0
                    row += 1

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_status_color(self, day_date):
        attendance = self.session.query(Attendance).filter_by(
            student_id=self.student_id,
            subject_id=self.subject_id,
            date=day_date
        ).first()
        if attendance and attendance.status in self.STATUS_COLORS:
            return self.STATUS_COLORS[attendance.status]
        return None

    def on_day_click(self, day_date):
        self.selected_date = day_date
        if not self.selected_status:
            messagebox.showwarning("Warning", "Please select attendance status first.")
            return

        try:
            dt_date = datetime.combine(day_date, datetime.min.time())

            existing = self.session.query(Attendance).filter_by(
                student_id=self.student_id,
                subject_id=self.subject_id,
                date=day_date
            ).first()

            if existing:
                AttendanceService.edit_attendance(self.session, existing.id, status=self.selected_status)
            else:
                AttendanceService.add_attendance(self.session,self.student_id,self.subject_id,self.selected_status,dt_date)

            self.session.commit()
            self.draw_calendar()

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", str(e))

    def set_status(self, status):
        self.selected_status = status
        for name, btn in self.status_buttons.items():
            if name == status:
                btn.configure(border_width=2, border_color="white")
            else:
                btn.configure(border_width=0)
