from flask import Blueprint, jsonify, session
import sqlite3

user_api = Blueprint("user_api", __name__)


@user_api.route("/api/profile")
def profile():

    user_email = session.get("user_email")

    if not user_email:
        return jsonify({
            "error": "User not logged in"
        }), 401

    connection = sqlite3.connect("diet_planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, age
        FROM users
        WHERE email = ?
    """, (user_email,))

    user = cursor.fetchone()

    connection.close()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "age": user[3]
    })