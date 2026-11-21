
from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "my_secret_key"

def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    if "username" in session:
        return render_template_string("""
            <h2>Welcome {{ username }}</h2>
            <a href="/logout">Logout</a>
        """, username=session["username"])

    return """
        <h2>User Authentication</h2>
        <a href="/register">Register</a><br><br>
        <a href="/login">Login</a>
    """

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(password) < 8:
            message = "Password must contain at least 8 characters."
        else:
            hashed_password = generate_password_hash(password)

            try:
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password)
                )

                conn.commit()
                conn.close()

                return redirect("/login")

            except sqlite3.IntegrityError:
                message = "Username already exists."

    return render_template_string("""
        <h2>Register</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required><br><br>
            <input type="password" name="password"
                   placeholder="Password" required><br><br>
            <button type="submit">Register</button>
        </form>
        <p>{{ message }}</p>
    """, message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["username"] = username
            return redirect("/")

        message = "Invalid username or password."

    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required><br><br>
            <input type="password" name="password"
                   placeholder="Password" required><br><br>
            <button type="submit">Login</button>
        </form>
        <p>{{ message }}</p>
    """, message=message)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

if __name__ == "__main__":
    create_table()
    port = int(os.environ.get("PORT", "5002"))
    app.run(host="127.0.0.1", port=port, debug=True)
