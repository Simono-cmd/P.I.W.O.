from app.database.database import SessionLocal
from app.models import Subject
from app.repositories.subject_repository import SubjectRepository

class SubjectService:

    @staticmethod
    def add_subject(session: SessionLocal, name: str) -> int:
        return SubjectRepository.add_subject(session, name)

    @staticmethod
    def delete_subject(session: SessionLocal, subject_id: int):
        SubjectRepository.delete_subject(session, subject_id)

    @staticmethod
    def edit_subject(session: SessionLocal, subject_id: int, name: str = None):
        SubjectRepository.edit_subject(session, subject_id, name)

    @staticmethod
    def get_subject(session: SessionLocal, subject_id: int):
        return SubjectRepository.get_subject(session, subject_id)

    @staticmethod
    def get_all_subjects(session: SessionLocal):
        subjects = session.query(Subject).all()
        return [subj.name for subj in subjects]
