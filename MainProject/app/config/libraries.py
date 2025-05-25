import subprocess
import sys

def check_and_install(package):
    try:
        __import__(package)
        print(f"{package} jest już zainstalowane.")
    except ImportError:
        print(f"{package} nie jest zainstalowane. Próbuję zainstalować...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} zostało pomyślnie zainstalowane.")

check_and_install("dotenv")
check_and_install("sqlalchemy")
check_and_install("psycopg2")
check_and_install("customtkinter")
check_and_install("openpyxl")
check_and_install("matplotlib")
