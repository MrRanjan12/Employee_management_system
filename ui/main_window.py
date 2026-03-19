from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget
)
from PyQt6.QtCore import Qt, QPoint

from ui.employee_page import EmployeePage
from ui.salary_page import SalaryPage


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db

        # Frameless window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showMaximized()

        self.old_pos = None

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= TOP BAR =================
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("""
            background-color: white;
            border-bottom: 1px solid #e5e7eb;
        """)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(15, 0, 15, 0)

        title = QLabel("EMS Dashboard")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #111827;
        """)

        # ===== BUTTONS =====
        btn_min = QPushButton("—")
        btn_max = QPushButton("▢")
        btn_close = QPushButton("✕")

        for btn in [btn_min, btn_max, btn_close]:
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #f3f4f6;
                }
            """)

        # ===== BUTTON ACTIONS =====
        btn_min.clicked.connect(self.showMinimized)

        def toggle_maximize():
            if self.isMaximized():
                self.showNormal()
                btn_max.setText("▢")
            else:
                self.showMaximized()
                btn_max.setText("❐")

        btn_max.clicked.connect(toggle_maximize)
        btn_close.clicked.connect(self.close)

        # ===== ADD TOP BAR =====
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(btn_min)
        top_layout.addWidget(btn_max)
        top_layout.addWidget(btn_close)

        top_bar.setLayout(top_layout)

        # ================= MAIN CONTENT =================
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # -------- SIDEBAR --------
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(240)
        sidebar_widget.setStyleSheet("background-color: #111827;")

        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(20, 20, 20, 10)
        sidebar.setSpacing(10)

        title_sidebar = QLabel("EMS Pro")
        title_sidebar.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)

        self.btn_employees = QPushButton("Employees")
        self.btn_salary = QPushButton("Salary")

        for btn in [self.btn_employees, self.btn_salary]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self.sidebar_btn())

        self.set_active(self.btn_employees)

        sidebar.addWidget(title_sidebar)
        sidebar.addSpacing(20)
        sidebar.addWidget(self.btn_employees)
        sidebar.addWidget(self.btn_salary)
        sidebar.addStretch()

        sidebar_widget.setLayout(sidebar)

        # -------- STACKED PAGES --------
        self.stack = QStackedWidget()

        # ✅ IMPORTANT FIX: db pass karo
        self.employee_page = EmployeePage(self.db)
        self.salary_page = SalaryPage(self.db)

        self.stack.addWidget(self.employee_page)
        self.stack.addWidget(self.salary_page)

        # Navigation
        self.btn_employees.clicked.connect(lambda: self.switch_page(0))
        self.btn_salary.clicked.connect(lambda: self.switch_page(1))

        content_layout.addWidget(sidebar_widget)
        content_layout.addWidget(self.stack)

        # ================= FINAL LAYOUT =================
        main_layout.addWidget(top_bar)
        main_layout.addLayout(content_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ================= SIDEBAR STYLE =================
    def sidebar_btn(self):
        return """
            QPushButton {
                color: #cbd5e1;
                padding: 10px;
                text-align: left;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1f2937;
                color: white;
            }
        """

    def set_active(self, active_btn):
        for btn in [self.btn_employees, self.btn_salary]:
            btn.setStyleSheet(self.sidebar_btn())

        active_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: white;
                padding: 10px;
                text-align: left;
                border-radius: 6px;
                border-left: 4px solid #3b82f6;
                font-weight: 600;
            }
        """)

    # ================= DRAG WINDOW =================
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    # ================= PAGE SWITCH =================
    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

        if index == 0:
            self.set_active(self.btn_employees)
        else:
            self.set_active(self.btn_salary)