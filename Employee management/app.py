
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary REAL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def home():
    search = request.args.get("search", "")

    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM employees
        WHERE name LIKE ? OR CAST(id AS TEXT) LIKE ?
    """, ('%' + search + '%', '%' + search + '%'))

    employees = cursor.fetchall()
    conn.close()

    return render_template_string("""
        <h2>Employee Management System</h2>

        <form action="/add" method="POST">
            <input name="name" placeholder="Employee Name" required>
            <input name="department" placeholder="Department" required>
            <input name="salary" type="number" step="0.01"
                   placeholder="Salary" required>
            <button type="submit">Add Employee</button>
        </form>

        <h3>Search Employees</h3>

        <form method="GET">
            <input name="search" placeholder="Search by name or ID"
                   value="{{ search }}">
            <button type="submit">Search</button>
        </form>

        <h3>Employee Records</h3>

        {% for employee in employees %}
            <p>
                ID: {{ employee[0] }} |
                Name: {{ employee[1] }} |
                Department: {{ employee[2] }} |
                Salary: {{ employee[3] }}

                <a href="/edit/{{ employee[0] }}">Edit</a>
                <a href="/delete/{{ employee[0] }}">Delete</a>
            </p>
        {% endfor %}
    """, employees=employees, search=search)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    department = request.form["department"]
    salary = request.form["salary"]

    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees (name, department, salary)
        VALUES (?, ?, ?)
    """, (name, department, salary))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        salary = request.form["salary"]

        cursor.execute("""
            UPDATE employees
            SET name=?, department=?, salary=?
            WHERE id=?
        """, (name, department, salary, id))

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM employees WHERE id=?", (id,))
    employee = cursor.fetchone()
    conn.close()

    if employee is None:
        return "Employee not found", 404

    return render_template_string("""
        <h2>Update Employee</h2>

        <form method="POST">
            <input name="name" value="{{ employee[1] }}" required>
            <input name="department" value="{{ employee[2] }}" required>
            <input name="salary" type="number" step="0.01"
                   value="{{ employee[3] }}" required>
            <button type="submit">Update</button>
        </form>
    """, employee=employee)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=5057)
