import re
from sqlalchemy import Column, Integer, String, ForeignKey
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
        if value < 0:
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

    # Relationships
    grades = relationship("Grade", backref="student")
    attendances = relationship("Attendance", backref="student")
