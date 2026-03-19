import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("ems.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Owner table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS owner(
            id INTEGER PRIMARY KEY,
            password TEXT
        )
        """)

        # Employees table (UPDATED)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            designation TEXT,
            department TEXT,
            salary REAL,
            deduction REAL DEFAULT 0
        )
        """)

        self.conn.commit()

    # ===== GENERAL EXECUTE =====
    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    # ===== OWNER =====
    def get_owner_password(self):
        cursor = self.execute("SELECT password FROM owner WHERE id=1")
        result = cursor.fetchone()
        return result[0] if result else None

    def set_owner_password(self, password):
        self.execute(
            "INSERT OR REPLACE INTO owner(id, password) VALUES(1, ?)",
            (password,)
        )

    # ===== EMPLOYEES =====
    def add_employee(self, name, designation, department, salary, deduction=0):
        self.execute("""
            INSERT INTO employees(name, designation, department, salary, deduction)
            VALUES (?, ?, ?, ?, ?)
        """, (name, designation, department, salary, deduction))

    def get_employee(self, emp_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
        return cursor.fetchone()

    def get_all_employees(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        return cursor.fetchall()