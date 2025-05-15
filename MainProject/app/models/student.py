import re
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy.orm import validates

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    pesel = Column(String, nullable=False)

    # Validations
    @validates('id')
    def validate_id(self, key, value):
        if value is not None and value < 0:
            raise ValueError("ID must not be lesser than 0")
        return value

    @validates('name', 'surname')
    def validate_name_and_surname(self, key, value):
        if not value.strip():
            raise ValueError(f"{key.capitalize()} cannot be empty")
        return value

    @validates('pesel')
    def validate_pesel(self, key, value):
        if not value.strip():
            raise ValueError("PESEL cannot be empty")
        if not re.match(r'^\d{11}$', value):
            raise ValueError("PESEL must be a valid 11-digit number")
        return value

    # toString
    def __str__(self):
        return f"Student #{self.id}: {self.name} {self.surname}, PESEL: {self.pesel}"

    # Relationships
    attendances = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    failures = relationship("Failure", back_populates="student", cascade="all, delete-orphan")
