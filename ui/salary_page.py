from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QFrame, QTextEdit,
    QFileDialog, QComboBox
)
from PyQt6.QtCore import Qt
from datetime import datetime


class SalaryPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.emp_data = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #eef2f7; color:black;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)

        header = QLabel("Salary Calculator & Slip Generator")
        header.setStyleSheet("font-size: 26px; font-weight: 700; color: #1f2937;")

        card = QFrame()
        card.setStyleSheet(self.card_style())

        card_layout = QVBoxLayout()

        # ================= EMPLOYEE SELECT =================
        self.employee_select = QComboBox()
        self.employee_select.addItem("Select Employee")

        self.load_employees()

        self.employee_select.currentIndexChanged.connect(self.on_employee_select)

        # ================= INPUT =================
        input_row = QHBoxLayout()

        self.basic = QLineEdit()
        self.basic.setPlaceholderText("Basic Salary")

        self.deduction = QLineEdit()
        self.deduction.setPlaceholderText("Deduction")

        input_row.addWidget(self.basic)
        input_row.addWidget(self.deduction)

        # ================= BUTTONS =================
        btn_row = QHBoxLayout()

        btn_calc = QPushButton("💰 Calculate")
        btn_slip = QPushButton("📄 Generate Slip")
        btn_download = QPushButton("⬇ Download")

        btn_calc.clicked.connect(self.calculate)
        btn_slip.clicked.connect(self.generate_slip)
        btn_download.clicked.connect(self.download_slip)

        btn_row.addWidget(btn_calc)
        btn_row.addWidget(btn_slip)
        btn_row.addWidget(btn_download)

        # ================= RESULT =================
        self.result = QLabel("Net Salary: ₹0")
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ================= SLIP =================
        self.slip_box = QTextEdit()
        self.slip_box.setReadOnly(True)

        # ================= ADD =================
        card_layout.addWidget(self.employee_select)
        card_layout.addLayout(input_row)
        card_layout.addLayout(btn_row)
        card_layout.addWidget(self.result)
        card_layout.addWidget(self.slip_box)

        card.setLayout(card_layout)

        main_layout.addWidget(header)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

    # ================= LOAD EMPLOYEES =================
    def load_employees(self):
        employees = self.db.get_all_employees()

        for emp in employees:
            emp_id = emp[0]
            name = emp[1]

            self.employee_select.addItem(name, emp_id)

    # ================= SELECT EMPLOYEE =================
    def on_employee_select(self, index):
        if index == 0:
            self.emp_data = None
            return

        emp_id = self.employee_select.currentData()
        self.emp_data = self.db.get_employee(emp_id)

        if self.emp_data:
            # DB STRUCTURE:
            # 0=id, 1=name, 2=role, 3=salary

            self.basic.setText(str(self.emp_data[3]))
            self.deduction.setText("0")

    # ================= CALCULATE =================
    def calculate(self):
        try:
            basic = float(self.basic.text() or 0)
            deduction = float(self.deduction.text() or 0)

            net = basic - deduction

            self.result.setText(f"Net Salary: ₹{net:,.2f}")

        except:
            self.result.setText("Invalid Input")

    # ================= GENERATE SLIP =================
    def generate_slip(self):
        if not self.emp_data:
            self.slip_box.setText("⚠ Please select an employee")
            return

        try:
            name = self.emp_data[1]
            role = self.emp_data[2]
            basic = float(self.emp_data[3])
            deduction = float(self.deduction.text() or 0)

            net = basic - deduction

            hra = basic * 0.40
            bonus = basic * 0.10
            pf = basic * 0.12

            date = datetime.now().strftime("%d %B %Y")

            slip = f"""
SALARY SLIP

Name        : {name}
Role        : {role}
Date        : {date}

Basic       : ₹{basic:,.2f}
HRA         : ₹{hra:,.2f}
Bonus       : ₹{bonus:,.2f}
PF          : ₹{pf:,.2f}
Deduction   : ₹{deduction:,.2f}

Net Salary  : ₹{net:,.2f}

System Generated
"""

            self.slip_box.setText(slip)

        except:
            self.slip_box.setText("Error generating slip")

    # ================= DOWNLOAD =================
    def download_slip(self):
        content = self.slip_box.toPlainText()

        if not content.strip():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Slip", "salary_slip.txt", "Text Files (*.txt)"
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

    # ================= STYLE =================
    def card_style(self):
        return """
        QFrame {
            background-color: white;
            border-radius: 14px;
            padding: 20px;
        }
        """