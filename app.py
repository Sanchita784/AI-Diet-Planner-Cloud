from flask import Flask, render_template, request, session, redirect
from database.db import create_database
from ai.diet_generator import generate_diet_plan
from cloud.cloudinary_config import upload_file

from database.api.user_api import user_api
from database.api.diet_api import diet_api
from database.api.diet_history_api import diet_history_api
from database.api.uploaded_files_api import uploaded_files_api

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from dotenv import load_dotenv

import sqlite3
import os


# Load environment variables
load_dotenv()


# Create Flask application
app = Flask(__name__)


# Secret key from .env
app.secret_key = os.getenv("FLASK_SECRET_KEY")


# Create database
create_database()


# Register APIs
app.register_blueprint(user_api)
app.register_blueprint(diet_api)
app.register_blueprint(diet_history_api)
app.register_blueprint(uploaded_files_api)


# ---------------- HOME ----------------

@app.route("/")
def home():

    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]

        # Hash password before storing
        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect("diet_planner.db")
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO users
                (name, email, password, age)
                VALUES (?, ?, ?, ?)
            """, (
                name,
                email,
                hashed_password,
                age
            ))

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return "Email already registered."

        connection.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("diet_planner.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, email, password, age
            FROM users
            WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user[3], password):

            user_age = user[4]

            session["user_age"] = user_age
            session["user_email"] = email

            # Go to protected dashboard
            return redirect("/dashboard")

        return "Invalid email or password."

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    # User must be logged in
    if "user_email" not in session:

        return redirect("/login")

    return render_template(
        "dashboard.html",
        user_age=session.get("user_age")
    )


# ---------------- GOAL ----------------

@app.route("/goal")
def goal():

    if "user_email" not in session:

        return redirect("/login")

    return render_template("goal.html")


# ---------------- DIET ----------------

@app.route("/diet", methods=["GET", "POST"])
def diet():

    if "user_email" not in session:

        return redirect("/login")

    if request.method == "POST":

        goal = request.form["goal"]

        age = session.get("user_age")

        plan = generate_diet_plan(age, goal)

        connection = sqlite3.connect("diet_planner.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO diet_history
            (
                user_email,
                goal,
                breakfast,
                lunch,
                evening_snack,
                dinner
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session.get("user_email"),
            goal,
            plan["Breakfast"],
            plan["Lunch"],
            plan["Evening Snack"],
            plan["Dinner"]
        ))

        connection.commit()
        connection.close()

        return render_template(
            "diet.html",
            plan=plan,
            goal=goal
        )

    return redirect("/goal")


# ---------------- HISTORY ----------------

@app.route("/history")
def history():

    if "user_email" not in session:

        return redirect("/login")

    user_email = session.get("user_email")

    connection = sqlite3.connect("diet_planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM diet_history
        WHERE user_email = ?
        ORDER BY created_at DESC
    """, (user_email,))

    diet_history = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        diet_history=diet_history
    )


# ---------------- CLOUD UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_email" not in session:
        return redirect("/login")

    if request.method == "POST":

        file = request.files.get("file")

        if not file or file.filename == "":
            return "No file selected."

        allowed_extensions = {
            "pdf",
            "jpg",
            "jpeg",
            "png"
        }

        filename = file.filename
        extension = filename.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            return "Invalid file type. Only PDF, JPG, JPEG and PNG files are allowed."

        # Maximum file size: 5 MB
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)

        if file_size > 5 * 1024 * 1024:
            return "File too large. Maximum file size is 5 MB."

        file_url = upload_file(file)

        connection = sqlite3.connect("diet_planner.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO uploaded_files
            (
                user_email,
                file_name,
                cloud_url
            )
            VALUES (?, ?, ?)
        """, (
            session.get("user_email"),
            filename,
            file_url
        ))

        connection.commit()
        connection.close()

        return f"""
        <h1>File Uploaded Successfully!</h1>

        <p>Your document has been stored in Cloudinary.</p>

        <p>Cloud Storage URL:</p>

        <a href="{file_url}" target="_blank">
            Open Uploaded File
        </a>

        <br><br>

        <a href="/dashboard">
            Back to Dashboard
        </a>
        """

    return render_template("upload.html")



# ---------------- UPLOADED FILES ----------------

@app.route("/files")
def files():

    if "user_email" not in session:

        return redirect("/login")

    user_email = session.get("user_email")

    connection = sqlite3.connect("diet_planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM uploaded_files
        WHERE user_email = ?
        ORDER BY uploaded_at DESC
    """, (user_email,))

    uploaded_files = cursor.fetchall()

    connection.close()

    return render_template(
        "files.html",
        uploaded_files=uploaded_files
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    app.run(debug=True)