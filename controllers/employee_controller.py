from models.employee import Employee


class EmployeeController:
    def __init__(self, db):
        self.db = db

    # ---------------- ADD ----------------
    def add_employee(self, emp: Employee):
        self.db.execute(
            "INSERT INTO employees(name, role, salary) VALUES(?,?,?)",
            (emp.name, emp.role, emp.salary)
        )

    # ---------------- GET ALL ----------------
    def get_all(self):
        cursor = self.db.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        return [Employee(*row) for row in rows]

    # ---------------- DELETE ----------------
    def delete(self, emp_id):
        self.db.execute("DELETE FROM employees WHERE id=?", (emp_id,))

    # ---------------- UPDATE ----------------
    def update(self, emp: Employee):
        self.db.execute(
            "UPDATE employees SET name=?, role=?, salary=? WHERE id=?",
            (emp.name, emp.role, emp.salary, emp.id)
        )

    # ---------------- SEARCH ----------------
    def search(self, keyword):
        cursor = self.db.execute(
            "SELECT * FROM employees WHERE name LIKE ? OR id LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        rows = cursor.fetchall()
        return [Employee(*row) for row in rows]