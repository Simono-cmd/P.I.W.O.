from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy.orm import validates
from datetime import datetime


class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    status = Column(String, nullable=False) #present/absent/excused/late
    date = Column(DateTime, nullable=False)

    # Validations

    @validates('id', 'student_id', 'subject_id')
    def validate_ids(self, key, value):
        if value < 0:
            raise ValueError(f"{key.capitalize()} must not be negative")
        return value

    @validates('status')
    def validate_status(self, key, value):
        allowed_statuses = ['present', 'absent', 'excused', 'late']
        if value not in allowed_statuses:
            raise ValueError(f"Status must be one of {', '.join(allowed_statuses)}")
        return value

    @validates('date')
    def validate_date(self, key, value):
        if not value:
            return datetime.now()
        if not isinstance(value, datetime):
            raise ValueError("Insert date in a datetime format")
        return value

    # toString
    def __str__(self):
        return f"Id: {self.id}, StudentID: {self.student_id}, SubjectID: {self.subject_id}, Status: {self.status}, Date: {self.date}"

    #ORM Relationships
    student = relationship("Student", back_populates="attendances")
    subject = relationship("Subject", back_populates="attendances")

