from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from utils.security import hash_password, verify_password


class LoginWindow(QWidget):
    def __init__(self, db, on_login_success):
        super().__init__()
        self.db = db
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Employee Management System")
        self.resize(1000, 650)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background (blur-like soft color)
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #eef2f7;
            }
        """)

        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Card =====
        card = QWidget()
        card.setFixedSize(420, 420)
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(15)

        # Logo / Title
        title = QLabel("EMS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #335;
        """)

        subtitle = QLabel("Sign in to continue")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: gray; font-size: 13px;")

        # ===== Email Field =====

        # ===== Password Field =====
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 14px;
                color: gray;                    
            }
            QLineEdit:focus {
                border: 1px solid #0078D4;
            }
        """)

        # Forgot password
      

        # ===== Button =====
        self.btn = QPushButton("Log In")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #0a66c2;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #004182;
            }
        """)
        self.btn.clicked.connect(self.handle_login)

        # Divider
        divider = QLabel("────────  or sign in with  ────────")
        divider.setAlignment(Qt.AlignmentFlag.AlignCenter)
        divider.setStyleSheet("color: gray; font-size: 12px;")

        # Social buttons (UI only)
       

        # Footer
        footer = QLabel("Contact admin for access")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 12px;")

        # Add all
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        
        card_layout.addWidget(self.password)
       
        card_layout.addWidget(self.btn)
        card_layout.addWidget(divider)
        
        card_layout.addWidget(footer)

        card.setLayout(card_layout)

        container_layout.addWidget(card)
        container.setLayout(container_layout)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

    # ===== SAME LOGIC (UNCHANGED) =====
    def handle_login(self):
        stored_password = self.db.get_owner_password()

        if not stored_password:
            new_pass = hash_password(self.password.text())
            self.db.set_owner_password(new_pass)
            QMessageBox.information(self, "Success", "Password Set Successfully!")
            self.on_login_success()
            return

        if verify_password(self.password.text(), stored_password):
            self.on_login_success()
        else:
            QMessageBox.warning(self, "Error", "Invalid Password")