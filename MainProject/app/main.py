from MainProject.app.database.database import SessionLocal
from MainProject.app.gui.main_window import MainWindow

session = SessionLocal()
try:
    app = MainWindow(session)
    app.run()
    session.close()
finally:
    session.commit()
    session.close()


# TODO
# 1. podpiac raporty
# 2. ogarnac wyjatki


# dotenv
# sqlalchemy
# psycopg2
# customtkinkter
# openpyxl
# matplotlib