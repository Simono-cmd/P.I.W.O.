from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from app.database.database import SessionLocal
from app.models.subject import Subject


class SubjectRepository:

    @staticmethod
    def add_subject(name: str) -> Subject:
        session = SessionLocal()
        try:
            subject = Subject(name=name)
            session.add(subject)
            session.comit()
            return subject
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete_subject(subject_id: int):
        session = SessionLocal()
        try:
            subject = session.query(Subject).get(subject_id)
            session.delete(subject)
            session.comit()
            return subject
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def edit_subject(subject_id: int, name: str = None):
        session = SessionLocal()
        try:
            subject = session.query(Subject).get(subject_id)
            if subject is None:
                raise NoResultFound("Subject with id {} not found".format(subject_id))

            if name: subject.name = name
            session.comit()
            return subject
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_subject(subject_id: int):
        session = SessionLocal()
        try:
            subject = session.query(Subject).get(subject_id)
            if subject is None:
                raise NoResultFound("Subject with id {} not found".format(subject_id))
            return subject
        finally:
            session.close()