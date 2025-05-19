import pytest
from sqlalchemy.exc import NoResultFound

from app.database.database import SessionLocal
from app.repositories.grade_repository import GradeRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.subject_repository import SubjectRepository


def test_grade_repository():
    session = SessionLocal()

    try:

        # student
        name = "Jan"
        surname = "Kowalski"
        pesel = "11111111111"
        student_id = StudentRepository.add_student(session, name, surname, pesel)

        # subject
        name = "Python"
        subject_id = SubjectRepository.add_subject(session, name)

        form = "short test"
        worth = 5
        grade_id = GradeRepository.add_grade(session, student_id, subject_id, form, worth)
        grade = GradeRepository.get_grade(session, grade_id)

        assert grade is not None
        assert grade.id == grade_id
        assert grade.subject_id == subject_id
        assert grade.student_id == student_id
        assert grade.form == form
        assert grade.worth == worth

        form = "test"
        worth = 4
        GradeRepository.edit_grade(session, grade_id, form = form, worth = worth)
        grade = GradeRepository.get_grade(session, grade_id)

        assert grade is not None
        assert grade.id == grade_id
        assert grade.subject_id == subject_id
        assert grade.student_id == student_id
        assert grade.form == form
        assert grade.worth == worth

        GradeRepository.delete_grade(session, grade_id)
        with pytest.raises(NoResultFound):
            GradeRepository.get_grade(session, grade_id)
    finally:
        session.rollback()
        session.close()
