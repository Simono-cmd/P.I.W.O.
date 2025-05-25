from MainProject.app.database.database import SessionLocal
from MainProject.app.gui.main_window import MainWindow

session = SessionLocal()

print(
    """
    
                                        ╔═══════════════════════════════════╗
                                        ║         PROJECT \033[93mP.I.W.O\033[0m           ║
                                        ╠═══════════════════════════════════╣
                                        ║   Authors : Szymon Trauth         ║
                                        ║             Michał Maksymiuk      ║
                                        ║                                   ║
                                        ║            2025 PJATK             ║
                                        ╚═══════════════════════════════════╝
                                        
    """
)

try:
    print("\033[92mrunning")
    app = MainWindow(session)
    app.run()
finally:
    session.commit()
    session.close()
    print("\033[91mshut down")









