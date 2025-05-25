from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from MainProject.app.database.database import Base

class Failure(Base):
    __tablename__ = 'failures'

    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, primary_key=True,)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False, primary_key=True,)

    # Validations
    @validates('student_id', 'subject_id')
    def validate_id(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key.capitalize()} must not be lesser than 0")
        return value



    # Relationships
    student = relationship("Student", back_populates="failures")
    subject = relationship("Subject", back_populates="failures")