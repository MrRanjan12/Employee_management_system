import sqlite3
import os
import sys


def get_db_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "ems.db")


class Database:
    def __init__(self):
        db_path = get_db_path()
        self.conn = sqlite3.connect(db_path)
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

        # ✅ UPDATED Employees table (MATCH UI)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            salary REAL
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
    def add_employee(self, name, role, salary):
        self.execute("""
            INSERT INTO employees(name, role, salary)
            VALUES (?, ?, ?)
        """, (name, role, salary))

    def update_employee(self, emp_id, name, role, salary):
        self.execute("""
            UPDATE employees
            SET name=?, role=?, salary=?
            WHERE id=?
        """, (name, role, salary, emp_id))

    def delete_employee(self, emp_id):
        self.execute("DELETE FROM employees WHERE id=?", (emp_id,))

    def get_employee(self, emp_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
        return cursor.fetchone()

    def get_all_employees(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        return cursor.fetchall()

    def search_employees(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM employees
            WHERE name LIKE ? OR role LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))
        return cursor.fetchall()