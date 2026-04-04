from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__, template_folder="templates")
app.secret_key = "secret"

# ✅ Database connection (FIXED)
def get_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database.db")
    return sqlite3.connect(db_path)

# ✅ Create tables
conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    name TEXT,
    amount REAL
)
""")

conn.commit()
conn.close()

# ✅ Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = get_db()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("register.html")

# ✅ Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = u
            return redirect("/dashboard")

    return render_template("login.html")

# ✅ Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]

        conn = get_db()
        conn.execute(
            "INSERT INTO expenses (user, name, amount) VALUES (?, ?, ?)",
            (session["user"], name, amount)
        )
        conn.commit()
        conn.close()

    conn = get_db()
    data = conn.execute(
        "SELECT name, amount FROM expenses WHERE user=?",
        (session["user"],)
    ).fetchall()
    conn.close()

    total = sum([row[1] for row in data])

    return render_template("dashboard.html", expenses=data, total=total)

# ✅ Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)