from datetime import datetime

import pytest
from sqlalchemy.exc import NoResultFound

from MainProject.app.database.database import SessionLocal
from MainProject.app.repositories.attendance_repository import AttendanceRepository
from MainProject.app.repositories.grade_repository import GradeRepository
from MainProject.app.repositories.student_repository import StudentRepository
from MainProject.app.repositories.subject_repository import SubjectRepository


def test_student_repository():

    session = SessionLocal()
    try:

        # add
        name = "Jan"
        surname = "Kowalski"
        pesel = "11111111111"
        student_id = StudentRepository.add_student(session, name, surname, pesel)
        student_from_db = StudentRepository.get_student(session, student_id)

        assert student_from_db is not None
        assert student_from_db.id == student_id
        assert student_from_db.name == name
        assert student_from_db.surname == surname
        assert student_from_db.pesel == pesel

        # edit
        name = "Eryk"
        surname = "Stanislawski"
        pesel = "22222222222"
        StudentRepository.edit_student(session, student_id, name, surname, pesel)
        student_from_db = StudentRepository.get_student(session, student_id)

        assert student_from_db is not None
        assert student_from_db.id == student_id
        assert student_from_db.name == name
        assert student_from_db.surname == surname
        assert student_from_db.pesel == pesel

        StudentRepository.delete_student(session, student_id)
        with pytest.raises(NoResultFound):
            StudentRepository.get_student(session, student_id)
    finally:
        session.rollback()
        session.close()


    #when we delete student do grades and attendances disappear

    session = SessionLocal()
    try:

        student1 = StudentRepository.add_student(session=session, name="Grzyb", surname="Wielki", pesel="11111111111")
        subject1=SubjectRepository.add_subject(session=session, name ="GigaPython")
        grade1= GradeRepository.add_grade(session=session, student_id=student1, subject_id=subject1, form="test", worth=5)
        attendance1=AttendanceRepository.add_attendance(session=session, student_id=student1, subject_id=subject1, status="present", date_of=datetime.now())

        StudentRepository.delete_student(session=session, student_id=student1)
        SubjectRepository.delete_subject(session=session, subject_id=subject1)

        with pytest.raises(NoResultFound):
            AttendanceRepository.get_attendance(session=session, attendance_id=attendance1)

        with pytest.raises(NoResultFound):
            GradeRepository.get_grade(session=session, grade_id=grade1)
    finally:
        session.rollback()
        session.close()