
from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def contact():
    result = ""

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        result = "Message submitted successfully!"

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact Form</title>
    </head>
    <body>
        <h2>Contact Us</h2>

        <form method="POST">
            <input type="text" name="name"
                   placeholder="Enter Name" required><br><br>

            <input type="email" name="email"
                   placeholder="Enter Email" required><br><br>

            <textarea name="message"
                      placeholder="Enter Message" required></textarea><br><br>

            <button type="submit">Submit</button>
        </form>

        <p>{{ result }}</p>
    </body>
    </html>
    """, result=result)

if __name__ == "__main__":
    create_table()
    port = int(os.environ.get("PORT", "5003"))
    app.run(host="127.0.0.1", port=port, debug=True)
