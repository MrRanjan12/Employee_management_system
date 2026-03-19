from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QSizePolicy, QFrame, QHeaderView
)
from PyQt6.QtCore import Qt
from controllers.employee_controller import EmployeeController
from models.employee import Employee


class EmployeePage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.controller = EmployeeController(db)
        self.selected_id = None
        self.init_ui()

    def init_ui(self):
        # ===== MAIN BACKGROUND =====
        self.setStyleSheet("background-color: #eef2f7;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(18)

        # ===== HEADER =====
        header = QLabel("Employee Management")
        header.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            color: #1f2937;
            border-radius:12px
        """)

        # ===== SEARCH =====
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  Search employees...")
        self.search.textChanged.connect(self.search_data)
        self.search.setMinimumHeight(45)
        self.search.setStyleSheet(self.search_style())

        # ===== FORM CARD =====
        form_card = QFrame()
        form_card.setStyleSheet(self.card_style())

        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        input_row = QHBoxLayout()
        input_row.setSpacing(12)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Employee Name")
        self.name.setStyleSheet(self.input_style())

        self.role = QLineEdit()
        self.role.setPlaceholderText("Role")
        self.role.setStyleSheet(self.input_style())

        self.salary = QLineEdit()
        self.salary.setPlaceholderText("Salary")
        self.salary.setStyleSheet(self.input_style())

        input_row.addWidget(self.name, 2)
        input_row.addWidget(self.role, 2)
        input_row.addWidget(self.salary, 1)

        # ===== BUTTONS =====
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        btn_add = QPushButton("➕ Add")
        btn_update = QPushButton("🔄 Update")
        btn_delete = QPushButton("🗑 Delete")

        btn_add.setStyleSheet(self.primary_btn())
        btn_update.setStyleSheet(self.secondary_btn())
        btn_delete.setStyleSheet(self.danger_btn())

        btn_add.clicked.connect(self.add_employee)
        btn_update.clicked.connect(self.update_employee)
        btn_delete.clicked.connect(self.delete_employee)

        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_update)
        btn_row.addWidget(btn_delete)
        btn_row.addStretch()

        form_layout.addLayout(input_row)
        form_layout.addLayout(btn_row)
        form_card.setLayout(form_layout)

        # ===== TABLE CARD =====
        table_card = QFrame()
        table_card.setStyleSheet(self.card_style())

        table_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Role", "Salary"])
        self.table.cellClicked.connect(self.select_row)

        # ===== COLUMN SIZE (BALANCED LIKE IMAGE) =====
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        # ===== ROW HEIGHT =====
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setVisible(False)

        # ===== TABLE STYLE =====
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                gridline-color: #e5e7eb;
                border-radius: 10px;
                color:black;
            }

            QHeaderView::section {
                background-color: #f3f4f6;
                padding: 14px;
                border: none;
                border-bottom: 1px solid #e5e7eb;
                font-weight: 600;
                color: #374151;
                color: black;
            }

            QTableWidget::item {
                padding-left: 12px;
                border-bottom: 1px solid #f1f5f9;
            }

            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: black;
            }
        """)

        self.table.setAlternatingRowColors(False)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        table_layout.addWidget(self.table)
        table_card.setLayout(table_layout)

        # ===== ADD ALL =====
        main_layout.addWidget(header)
        main_layout.addWidget(self.search)
        main_layout.addWidget(form_card)
        main_layout.addWidget(table_card)

        main_layout.setStretch(3, 1)
        self.setLayout(main_layout)

        self.load_data()

    # ================= STYLES =================
    def card_style(self):
        return """
            QFrame {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #e5e7eb;
                padding: 18px;
                color:gray;
        """

    def search_style(self):
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                color:gray;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
            }
        """

    def input_style(self):
        return """
            QLineEdit {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                color:gray;
            }
            QLineEdit:focus {
                background-color: white;
                border: 1px solid #3b82f6;
                color:gray;
            }
        """

    def primary_btn(self):
        return """
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 10px 18px;
                border-radius: 10px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """

    def secondary_btn(self):
        return """
            QPushButton {
                background-color: #f3f4f6;
                color: #111827;
                padding: 10px 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """

    def danger_btn(self):
        return """
            QPushButton {
                background-color: #ef4444;
                color: white;
                padding: 10px 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """

    # ================= LOGIC (UNCHANGED) =================
    def load_data(self):
        data = self.controller.get_all()
        self.populate_table(data)

    def populate_table(self, data):
        self.table.setRowCount(len(data))

        for row, emp in enumerate(data):
            id_item = QTableWidgetItem(str(emp.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, id_item)

            self.table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.table.setItem(row, 2, QTableWidgetItem(emp.role))

            salary_item = QTableWidgetItem(f"${emp.salary:,.2f}")
            salary_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, salary_item)

    def search_data(self):
        keyword = self.search.text()
        data = self.controller.search(keyword)
        self.populate_table(data)

    def add_employee(self):
        try:
            emp = Employee(
                name=self.name.text(),
                role=self.role.text(),
                salary=float(self.salary.text())
            )
            self.controller.add_employee(emp)
            self.clear_fields()
            self.load_data()
        except:
            QMessageBox.warning(self, "Error", "Invalid Input")

    def select_row(self, row, column):
        self.selected_id = int(self.table.item(row, 0).text())
        self.name.setText(self.table.item(row, 1).text())
        self.role.setText(self.table.item(row, 2).text())
        self.salary.setText(self.table.item(row, 3).text().replace("$", "").replace(",", ""))

    def update_employee(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Error", "Select an employee first")
            return

        try:
            emp = Employee(
                id=self.selected_id,
                name=self.name.text(),
                role=self.role.text(),
                salary=float(self.salary.text())
            )
            self.controller.update(emp)
            self.clear_fields()
            self.load_data()
        except:
            QMessageBox.warning(self, "Error", "Invalid Input")

    def delete_employee(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Error", "Select an employee first")
            return

        self.controller.delete(self.selected_id)
        self.clear_fields()
        self.load_data()

    def clear_fields(self):
        self.selected_id = None
        self.name.clear()
        self.role.clear()
        self.salary.clear()