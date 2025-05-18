from app.database.database import SessionLocal
from app.repositories.subject_repository import SubjectRepository

class SubjectService:

    @staticmethod
    def add_subject_inside_another_transaction(session: SessionLocal, name: str) -> int:
        return SubjectRepository.add_subject_inside_another_transaction(session, name)

    @staticmethod
    def delete_subject_inside_another_transaction(session: SessionLocal, subject_id: int):
        SubjectRepository.delete_subject_inside_another_transaction(session, subject_id)

    @staticmethod
    def edit_subject_inside_another_transaction(session: SessionLocal, subject_id: int, name: str = None):
        SubjectRepository.edit_subject_inside_another_transaction(session, subject_id, name)

    @staticmethod
    def get_subject_inside_another_transaction(session: SessionLocal, subject_id: int):
        return SubjectRepository.get_subject_inside_another_transaction(session, subject_id)