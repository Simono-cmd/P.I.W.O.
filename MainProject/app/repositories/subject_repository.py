from sqlalchemy.exc import NoResultFound
from MainProject.app.database.database import SessionLocal
from MainProject.app.models import Student, Attendance
from MainProject.app.models.subject import Subject


class SubjectRepository:

    @staticmethod
    def add_subject(session: SessionLocal, name: str) -> int:
        subject = Subject(name=name)
        session.add(subject)
        session.flush()
        return subject.id

    @staticmethod
    def delete_subject(session: SessionLocal, subject_id: int):
        subject = session.query(Subject).get(subject_id)
        session.delete(subject)
        session.flush()


    @staticmethod
    def edit_subject(session: SessionLocal, subject_id: int, name: str = None):
        subject = session.query(Subject).get(subject_id)
        if subject is None:
            raise NoResultFound("Subject with id {} not found".format(subject_id))

        if name: subject.name = name
        session.flush()


    @staticmethod
    def get_subject(session: SessionLocal, subject_id: int):
        subject = session.query(Subject).get(subject_id)
        if subject is None:
            raise NoResultFound("Subject with id {} not found".format(subject_id))
        return subject

    @staticmethod
    def delete_subject_name(session: SessionLocal, subject_name: str):
        subject = session.query(Subject).get(subject_name)
        session.delete(subject)
        session.flush()

    @staticmethod
    def get_students_enrolled_in_subject(session: SessionLocal, subject_name: int):
        return session.query(Student) \
            .select_from(Attendance) \
            .join(Subject, Subject.id == Attendance.subject_id) \
            .join(Student, Student.id == Attendance.student_id) \
            .filter(Subject.name == subject_name and Attendance.subject_id == Subject.id) \
            .all()

    @staticmethod
    def find_subject_id_by_name(session: SessionLocal, subject_name: str):
        return session.query(Subject.id).filter(Subject.name == subject_name).scalar()