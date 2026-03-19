import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from database.db import Database
from ui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)

    # Load styles (safe loading)
    try:
        with open("assets/styles.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ styles.qss not found, running without styling")

    # Initialize database
    db = Database()

    main_window = None

    def on_login_success():
        nonlocal main_window

        print("✅ Login Successful")
        login.close()

        from ui.main_window import MainWindow
        main_window = MainWindow(db)
        main_window.show()

    login = LoginWindow(db, on_login_success)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()