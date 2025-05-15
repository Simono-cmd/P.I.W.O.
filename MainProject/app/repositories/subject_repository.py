from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from app.database.database import SessionLocal
from app.models.subject import Subject


class SubjectRepository:

    @staticmethod
    def add_subject(name: str) -> int:
        session = SessionLocal()
        try:
            subject = Subject(name=name)
            session.add(subject)
            session.commit()
            return subject.id
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
            session.commit()
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
            session.commit()
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


#######################################################################################



    @staticmethod
    def add_subject_inside_another_transaction(session: SessionLocal, name: str) -> int:
        subject = Subject(name=name)
        session.add(subject)
        session.flush()
        return subject.id

    @staticmethod
    def delete_subject_inside_another_transaction(session: SessionLocal, subject_id: int):
        subject = session.query(Subject).get(subject_id)
        session.delete(subject)
        session.flush()


    @staticmethod
    def edit_subject_inside_another_transaction(session: SessionLocal, subject_id: int, name: str = None):
        subject = session.query(Subject).get(subject_id)
        if subject is None:
            raise NoResultFound("Subject with id {} not found".format(subject_id))

        if name: subject.name = name
        session.flush()


    @staticmethod
    def get_subject_inside_another_transaction(session: SessionLocal, subject_id: int):
        subject = session.query(Subject).get(subject_id)
        if subject is None:
            raise NoResultFound("Subject with id {} not found".format(subject_id))
        session.flush()
        return subject