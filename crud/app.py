
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template_string("""
        <h2>Student Management</h2>

        <form action="/add" method="POST">
            <input name="name" placeholder="Name" required>
            <input name="email" type="email"
                   placeholder="Email" required>
            <button type="submit">Add Student</button>
        </form>

        <h3>Student Records</h3>

        {% for student in students %}
            <p>
                {{ student[0] }} - {{ student[1] }} - {{ student[2] }}

                <a href="/edit/{{ student[0] }}">Edit</a>
                <a href="/delete/{{ student[0] }}">Delete</a>
            </p>
        {% endfor %}
    """, students=students)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    email = request.form["email"]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        cursor.execute(
            "UPDATE students SET name=?, email=? WHERE id=?",
            (name, email, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()

    if student is None:
        return "Student not found", 404

    return render_template_string("""
        <h2>Edit Student</h2>

        <form method="POST">
            <input name="name" value="{{ student[1] }}" required>
            <input name="email" type="email"
                   value="{{ student[2] }}" required>
            <button type="submit">Update</button>
        </form>
    """, student=student)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(host="127.0.0.1", port=5001, debug=True)
