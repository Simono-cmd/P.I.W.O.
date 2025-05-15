from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy.orm import validates


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    form = Column(String, nullable=False) #test/short test/homework
    worth = Column(Integer, nullable=False) #1-6


    # Validations
    @validates('id', 'student_id', 'subject_id')
    def validate_fields(self, key, value):
        if value < 0:
            raise ValueError(f"{key.capitalize()} must not be lesser than 0")
        return value

    @validates('form')
    def validate_type(self, key, value):
        allowed_types = ['test', 'short test', 'homework']
        if value not in allowed_types:
            raise ValueError(f"Type must be one of {', '.join(allowed_types)}")
        return value

    @validates('worth')
    def validate_value(self, key, value):
        if not (1 <= value <= 6):
            raise ValueError("Grade value must be between 1 and 6")
        return value


    # toString
    def __str__(self):
        return (f"Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, "
                f"type='{self.type}', value={self.value})")

    # Relationships
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
