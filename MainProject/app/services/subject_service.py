from MainProject.app.database.database import SessionLocal
from MainProject.app.models import Subject, Student, Attendance
from MainProject.app.repositories.subject_repository import SubjectRepository

class SubjectService:

    @staticmethod
    def add_subject(session: SessionLocal, name: str) -> int:
        return SubjectRepository.add_subject(session, name)

    @staticmethod
    def delete_subject(session: SessionLocal, subject_id: int) -> None:
        SubjectRepository.delete_subject(session, subject_id)

    @staticmethod
    def delete_subject_name(session: SessionLocal, subject_name: str) -> None:
        SubjectRepository.delete_subject_name(session, subject_name)

    @staticmethod
    def edit_subject(session: SessionLocal, subject_id: int, name: str = None) -> None:
        SubjectRepository.edit_subject(session, subject_id, name)

    @staticmethod
    def get_subject(session: SessionLocal, subject_id: int) -> Subject:
        return SubjectRepository.get_subject(session, subject_id)

    @staticmethod
    def get_all_subjects(session: SessionLocal) -> list[Subject]:
        return session.query(Subject).all()

    @staticmethod
    def get_students_enrolled_in_subject(session: SessionLocal, subject_name: str) -> list[Student]:
        return SubjectRepository.get_students_enrolled_in_subject(session, subject_name)

    @staticmethod
    def find_subject_id_by_name(session: SessionLocal, subject_name: str) -> int:
        return SubjectRepository.find_subject_id_by_name(session, subject_name)